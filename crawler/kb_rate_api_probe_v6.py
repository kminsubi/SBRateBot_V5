# SBRateBot V5 - KB Savings ISA / IRP Official API Probe v6
import json, re, html
from pathlib import Path
import requests, urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE="https://www.kbsavings.com"
PAGE=BASE+"/websquare/websquare.jsp?w2xPath=/jsp/depositItemInfo/depositItemInfo.xml"
API=BASE+"/websquare/engine/callJsonService.jsp?serviceID=S_CommonItemService_getItemInfo"
OUT_JSON=Path("data/kb_rate_api_probe_v6.json")
OUT_TXT=Path("data/kb_rate_api_probe_v6.txt")

S=requests.Session()
S.headers.update({
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/142 Safari/537.36",
    "Accept":"application/json, text/plain, */*",
    "Origin":BASE,
    "Referer":PAGE,
})

def clean_text(value):
    if value is None:
        return ""
    value=html.unescape(str(value))
    value=re.sub(r"<br\s*/?>","\n",value,flags=re.I)
    value=re.sub(r"</?(?:p|div|tr|li|ul|ol|table|tbody|thead|span|strong|b|em)[^>]*>","\n",value,flags=re.I)
    value=re.sub(r"</?t[dh][^>]*>"," ",value,flags=re.I)
    value=re.sub(r"<[^>]+>"," ",value)
    value=re.sub(r"[ \t]+"," ",value)
    value=re.sub(r"\n\s*\n+","\n",value)
    return value.strip()

def parse_rate_candidates(text):
    text=clean_text(text)
    rates={"3m":[],"6m":[],"12m":[],"24m":[],"36m":[]}
    patterns=[
        r"(?P<term>3|6|12|24|36)\s*개월.{0,120}?(?P<rate>\d+(?:\.\d+)?)\s*%",
        r"(?P<rate>\d+(?:\.\d+)?)\s*%.{0,120}?(?P<term>3|6|12|24|36)\s*개월",
    ]
    for pat in patterns:
        for m in re.finditer(pat,text,flags=re.I|re.S):
            month=int(m.group("term"))
            rate=float(m.group("rate"))
            if 0 <= rate <= 10:
                key=f"{month}m"
                if rate not in rates[key]:
                    rates[key].append(rate)
    return rates

def normalize_response(payload):
    data=payload.get("DATA",payload)
    if not isinstance(data,dict):
        return {},[],[],[]
    result=data.get("RESULT") or {}
    info=data.get("RESULT_ITEM_INFO") or []
    summary=data.get("RESULT_ITEM_SUMMARY") or []
    files=data.get("RESULT_ITEM_FILE") or []
    if isinstance(result,list):
        result=result[0] if result else {}
    return result,info,summary,files

def try_request(item_code):
    payloads=[
        {"ITEM_CODE":item_code},
        {"SEARCH":{"ITEM_CODE":item_code}},
        {"data":{"ITEM_CODE":item_code}},
        {"DATA":{"ITEM_CODE":item_code}},
    ]
    last_error=None
    for idx,payload in enumerate(payloads,1):
        try:
            r=S.post(
                API,
                json=payload,
                timeout=30,
                verify=False,
                headers={
                    "Content-Type":"application/json;charset=UTF-8",
                    "X-Requested-With":"XMLHttpRequest",
                },
            )
            if r.status_code != 200:
                last_error=f"HTTP {r.status_code}"
                continue
            try:
                obj=r.json()
            except Exception:
                last_error=f"JSON parse failed: {r.text[:120]!r}"
                continue
            result,info,summary,files=normalize_response(obj)
            item_name=str(result.get("ITEM_NAME","")).strip()
            if item_name:
                return {
                    "ok":True,
                    "payload_no":idx,
                    "request_payload":payload,
                    "response":obj,
                    "result":result,
                    "info":info,
                    "summary":summary,
                    "files":files,
                }
            last_error="ITEM_NAME empty"
        except Exception as e:
            last_error=repr(e)
    return {"ok":False,"error":last_error}

def collect_text_blocks(info,summary):
    blocks=[]
    if isinstance(summary,list):
        for row in summary:
            if not isinstance(row,dict):
                continue
            texts=[row.get("TEXT1"),row.get("TEXT2"),row.get("TEXT3")]
            joined="\n".join(clean_text(x) for x in texts if x not in (None,""))
            if joined:
                blocks.append({
                    "source":"RESULT_ITEM_SUMMARY",
                    "gubn_code":str(row.get("GUBN_CODE","")),
                    "gubn_name":str(row.get("GUBN_NAME","")),
                    "text":joined,
                })
    if isinstance(info,list):
        for row in info:
            if not isinstance(row,dict):
                continue
            content=row.get("CONTENT_HTML") or row.get("CONTENT") or ""
            text=clean_text(content)
            if text:
                blocks.append({
                    "source":"RESULT_ITEM_INFO",
                    "gubn_code":str(row.get("GUBN_CODE","")),
                    "gubn_name":str(row.get("GUBN_NAME","")),
                    "text":text,
                })
    return blocks

def classify_product(item_name,blocks):
    full=item_name+"\n"+"\n".join(x["text"] for x in blocks)
    upper=full.upper()
    if "ISA정기예금" in full or ("ISA" in upper and "정기예금" in full):
        return "ISA"
    if "퇴직연금" in full or "DC형" in full or "DC/IRP" in upper or ("IRP" in upper and "정기예금" in full):
        return "IRP"
    return None

def merge_rate_candidates(blocks):
    merged={"3m":[],"6m":[],"12m":[],"24m":[],"36m":[]}
    rate_blocks=[]
    for block in blocks:
        is_rate=(
            block["gubn_code"]=="2809"
            or "이율" in block["gubn_name"]
            or "금리" in block["gubn_name"]
            or any(x in block["text"] for x in ["3개월","6개월","12개월","24개월","36개월"])
        )
        if not is_rate:
            continue
        cand=parse_rate_candidates(block["text"])
        rate_blocks.append({**block,"candidates":cand})
        for key,vals in cand.items():
            for val in vals:
                if val not in merged[key]:
                    merged[key].append(val)
    return merged,rate_blocks

def main():
    print("="*84)
    print("SBRateBot V5 KB ISA / IRP Official API Probe v6")
    print("="*84)

    print("[1] warm-up")
    try:
        r=S.get(PAGE+"&ITEM_CODE=IB13",timeout=30,verify=False)
        print("    HTTP:",r.status_code,"/ cookies:",len(S.cookies))
    except Exception as e:
        print("    warning:",e)

    results={"api":API,"products":[],"targets":{"ISA":[],"IRP":[]}}

    print("\n[2] IB01 ~ IB40 공식 상품조회")
    for number in range(1,41):
        code=f"IB{number:02d}"
        res=try_request(code)
        if not res["ok"]:
            print(f"  {code}: - ({res.get('error')})")
            continue

        item=res["result"]
        name=str(item.get("ITEM_NAME","")).strip()
        blocks=collect_text_blocks(res["info"],res["summary"])
        kind=classify_product(name,blocks)
        rates,rate_blocks=merge_rate_candidates(blocks)

        product={
            "item_code":code,
            "item_name":name,
            "type_code":item.get("TYPE_CODE"),
            "type_name":item.get("TYPE_NAME"),
            "grp_code":item.get("GRP_CODE"),
            "grp_name":item.get("GRP_NAME"),
            "payload_no":res["payload_no"],
            "request_payload":res["request_payload"],
            "classification":kind,
            "rate_candidates":rates,
            "rate_blocks":rate_blocks,
            "result":item,
        }
        results["products"].append(product)

        marker=""
        if kind:
            results["targets"][kind].append(product)
            marker=f" <<< {kind}"

        print(f"  {code}: {name}{marker}")
        if marker:
            print("       rate candidates:",rates)

    OUT_JSON.parent.mkdir(parents=True,exist_ok=True)
    OUT_JSON.write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")

    lines=["="*100,"SBRateBot V5 KB ISA / IRP Official API Probe v6","="*100,"","API: "+API,""]
    for kind in ("ISA","IRP"):
        lines += ["="*100,kind,"="*100]
        targets=results["targets"][kind]
        if not targets:
            lines += ["TARGET NOT FOUND",""]
            continue
        for product in targets:
            lines.append(f"ITEM_CODE : {product['item_code']}")
            lines.append(f"ITEM_NAME : {product['item_name']}")
            lines.append(f"TYPE      : {product['type_code']} / {product['type_name']}")
            lines.append(f"GROUP     : {product['grp_code']} / {product['grp_name']}")
            lines.append("RATE CANDIDATES:")
            lines.append(json.dumps(product["rate_candidates"],ensure_ascii=False,indent=2))
            lines.append("RATE BLOCKS:")
            for block in product["rate_blocks"]:
                lines.append(f"[{block['source']}] {block['gubn_code']} / {block['gubn_name']}")
                lines.append(block["text"][:6000])
                lines.append("candidates="+json.dumps(block["candidates"],ensure_ascii=False))
                lines.append("")
            lines.append("-"*100)

    lines += ["","="*100,"ALL DEPOSIT PRODUCTS","="*100]
    for product in results["products"]:
        lines.append(f"{product['item_code']} | {product['item_name']} | {product['classification'] or '-'}")

    OUT_TXT.write_text("\n".join(lines),encoding="utf-8")

    print("\n"+"="*84)
    print("완료")
    print("="*84)
    print("ISA targets:",[x["item_code"]+":"+x["item_name"] for x in results["targets"]["ISA"]])
    print("IRP targets:",[x["item_code"]+":"+x["item_name"] for x in results["targets"]["IRP"]])
    print("JSON:",OUT_JSON)
    print("TXT :",OUT_TXT)
    print("※ isa_rates.json / irp_rates.json은 수정하지 않습니다.")

if __name__=="__main__":
    main()
