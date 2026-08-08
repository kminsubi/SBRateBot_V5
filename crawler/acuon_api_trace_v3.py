import json, re
from pathlib import Path
from urllib.parse import urljoin
import requests

BASE="https://www.acuonsb.co.kr"
JS=BASE+"/js/ibanking/pdt/pdt0000001.js"
TARGETS={
 "ISA":{"name":"ISA정기예금","page":BASE+"/sv_dpt1201170.act","product_id":"1201170"},
 "IRP":{"name":"퇴직연금정기예금","page":BASE+"/sv_dpt0030180.act","product_id":"1201171"},
}
OUT=Path("data/acuon_api_trace_v3.json")
OUTTXT=Path("data/acuon_api_trace_v3.txt")

s=requests.Session()
s.headers.update({"User-Agent":"Mozilla/5.0 Chrome/142 Safari/537.36","Accept-Language":"ko-KR,ko;q=0.9","X-Requested-With":"XMLHttpRequest"})

def req(method,url,**kw):
    r=s.request(method,url,timeout=40,allow_redirects=True,**kw)
    if not r.encoding or r.encoding.lower()=="iso-8859-1":
        r.encoding=r.apparent_encoding or "utf-8"
    return r

def contexts(text,needle,before=2500,after=7000):
    out=[]
    for m in re.finditer(re.escape(needle),text):
        out.append(text[max(0,m.start()-before):min(len(text),m.end()+after)])
    return out

def endpoints(text):
    out=[]
    patterns=[
        r'url\s*:\s*["\']([^"\']+)["\']',
        r'\.(?:get|post)\(\s*["\']([^"\']+)["\']',
    ]
    for pat in patterns:
        for m in re.finditer(pat,text,re.I):
            u=m.group(1).strip()
            if u.startswith("/"): u=urljoin(BASE,u)
            if u not in out: out.append(u)
    return out

def ajax_blocks(text):
    out=[]
    for token in ("$.ajax","$.post","$.get","getProductInfo"):
        pos=0
        while True:
            i=text.find(token,pos)
            if i<0: break
            block=text[max(0,i-1500):min(len(text),i+6000)]
            if block not in out: out.append(block)
            pos=i+len(token)
    return out

def test_endpoint(url,pid,referer):
    result={"url":url,"attempts":[]}
    if not url.startswith("http"):
        return result
    payloads=[
        {"GD_NO":pid},{"gdNo":pid},{"gd_no":pid},{"productId":pid},
        {"product_id":pid},{"PD_CD":pid},{"pdCd":pid},{"pdtNo":pid},
        {"GD_CD":pid},{"gdCd":pid}
    ]
    for method,payload in [("GET",None)]+[(m,p) for p in payloads for m in ("GET","POST")]:
        try:
            kw={"headers":{"Referer":referer}}
            if payload:
                kw["params" if method=="GET" else "data"]=payload
            r=req(method,url,**kw)
            body=r.text
            ctype=(r.headers.get("Content-Type") or "").lower()
            jl="json" in ctype or body.lstrip().startswith(("{","["))
            item={"method":method,"payload":payload,"status":r.status_code,
                  "content_type":r.headers.get("Content-Type"),"length":len(r.content),
                  "json_like":jl,"head":body[:1200]}
            if jl:
                try:item["json"]=r.json()
                except:pass
            result["attempts"].append(item)
            if r.status_code==200 and jl:
                break
        except Exception as e:
            result["attempts"].append({"method":method,"payload":payload,"error":repr(e)})
    return result

def main():
    print("="*76)
    print("SBRateBot V5 Acuon ISA / IRP API Trace v3")
    print("="*76)
    for t in TARGETS.values():
        try:
            r=req("GET",t["page"])
            print("warmup",t["name"],r.status_code)
        except Exception as e: print("warmup FAIL",t["name"],e)

    print("\n[1] pdt0000001.js")
    r=req("GET",JS)
    print("HTTP:",r.status_code,"SIZE:",len(r.content))
    text=r.text
    fn=contexts(text,"getProductInfo")
    blocks=ajax_blocks(text)
    eps=endpoints(text)
    print("getProductInfo hits:",len(fn))
    print("AJAX blocks:",len(blocks))
    print("endpoint candidates:",len(eps))
    for e in eps: print("  ->",e)

    result={"common_js":{"url":r.url,"status":r.status_code,"size":len(r.content),
            "getProductInfo_contexts":fn,"ajax_blocks":blocks,"endpoint_candidates":eps},
            "targets":{}}

    candidates=[e for e in eps if e.startswith("http") and "acuonsb.co.kr" in e]
    print("\n[2] 후보 API 테스트")
    for kind,t in TARGETS.items():
        print("\n",kind,t["name"],t["product_id"])
        tests=[]
        for e in candidates:
            print(" TEST",e)
            x=test_endpoint(e,t["product_id"],t["page"])
            tests.append(x)
            if any(a.get("status")==200 and a.get("json_like") for a in x["attempts"]):
                print("   >>> JSON 후보 발견")
                break
        result["targets"][kind]={**t,"api_tests":tests}

    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    OUTTXT.write_text(
        "SBRateBot V5 Acuon API Trace v3\n\n"+
        "GETPRODUCTINFO\n"+json.dumps(fn,ensure_ascii=False,indent=2)+
        "\n\nAJAX BLOCKS\n"+json.dumps(blocks,ensure_ascii=False,indent=2)+
        "\n\nENDPOINTS\n"+json.dumps(eps,ensure_ascii=False,indent=2)+
        "\n\nTESTS\n"+json.dumps(result["targets"],ensure_ascii=False,indent=2),
        encoding="utf-8")
    print("\n완료:",OUT,OUTTXT)
    print("※ 기존 ISA/IRP 금리 데이터는 수정하지 않습니다.")

if __name__=="__main__":
    main()
