# SBRateBot V5 - KB Savings Mobile ISA / IRP Probe v5
import json, re, ssl, urllib.parse, urllib.request
from pathlib import Path

BASE="https://www.kbsavings.com"
SEEDS=[
    BASE+"/mobweb/main.do",
    BASE+"/mobweb/kiwisavings/eplusSavingsProd.do",
    BASE+"/mobweb/kiwicustomer/prt_fnce_prd_regt.do",
]
OUT_JSON=Path("data/kb_mobile_isa_irp_probe_v5.json")
OUT_TXT=Path("data/kb_mobile_isa_irp_probe_v5.txt")
CACHE=Path("data/kb_mobile_isa_irp_probe_v5_cache")
TARGETS=["ISA정기예금","ISA","퇴직연금 정기예금","퇴직연금","IRP","DC형","DC/IRP"]

CTX=ssl.create_default_context()
CTX.check_hostname=False
CTX.verify_mode=ssl.CERT_NONE

def fetch(url,timeout=70):
    req=urllib.request.Request(url,headers={
        "User-Agent":"Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/142 Mobile Safari/537.36",
        "Accept":"*/*","Referer":BASE+"/"})
    with urllib.request.urlopen(req,timeout=timeout,context=CTX) as r:
        raw=r.read()
        charset=r.headers.get_content_charset() or "utf-8"
        return {"url":r.geturl(),"status":r.status,"type":r.headers.get("Content-Type",""),
                "raw":raw,"text":raw.decode(charset,errors="replace")}

def absolute(base,value):
    return urllib.parse.urljoin(base,value)

def contexts(text,keyword,radius=900,limit=30):
    out=[]; low=text.lower(); key=keyword.lower(); pos=0
    while len(out)<limit:
        i=low.find(key,pos)
        if i<0: break
        out.append(text[max(0,i-radius):min(len(text),i+len(keyword)+radius)].replace("\r"," ").replace("\n"," "))
        pos=i+len(keyword)
    return out

def target_hits(text):
    out={}
    for kw in TARGETS:
        vals=contexts(text,kw)
        if vals: out[kw]=vals
    return out

def extract_links(text,base):
    out=set()
    patterns=[
        r'href\s*=\s*["\']([^"\']+)["\']',
        r'src\s*=\s*["\']([^"\']+)["\']',
        r'url\s*:\s*["\']([^"\']+)["\']',
        r'location(?:\.href)?\s*=\s*["\']([^"\']+)["\']',
        r'["\']([^"\']+\.do(?:\?[^"\']*)?)["\']',
        r'["\']([^"\']+\.json(?:\?[^"\']*)?)["\']',
    ]
    for pat in patterns:
        for value in re.findall(pat,text,flags=re.I):
            if value.startswith(("javascript:","data:","#","tel:","mailto:")): continue
            url=absolute(base,value)
            if "kbsavings.com" in url: out.add(url)
    return sorted(out)

def extract_identifiers(text):
    out=[]
    patterns={
        "ITEM_CODE":r'ITEM_CODE\s*[:=]\s*["\']?([A-Za-z0-9_-]+)',
        "itemCode":r'itemCode\s*[:=]\s*["\']?([A-Za-z0-9_-]+)',
        "gdsNo":r'gdsNo\s*[:=]\s*["\']?([A-Za-z0-9_-]+)',
        "goodsNo":r'goodsNo\s*[:=]\s*["\']?([A-Za-z0-9_-]+)',
        "prdNo":r'prdNo\s*[:=]\s*["\']?([A-Za-z0-9_-]+)',
        "prodNo":r'prodNo\s*[:=]\s*["\']?([A-Za-z0-9_-]+)',
        "lonGdsNo":r'lonGdsNo\s*[:=]\s*["\']?([A-Za-z0-9_-]+)',
    }
    for name,pat in patterns.items():
        for m in re.finditer(pat,text,flags=re.I):
            out.append({"type":name,"value":m.group(1),
                "context":text[max(0,m.start()-500):min(len(text),m.end()+1200)].replace("\r"," ").replace("\n"," ")})
    return out

def extract_endpoints(text,base):
    out=set()
    patterns=[
        r'["\']([^"\']+\.(?:do|json|ajax)(?:\?[^"\']*)?)["\']',
        r'["\']((?:/|https?://)[^"\']*(?:rate|interest|intr|saving|deposit|pension|retire|isa|irp|product|prod|goods|gds)[^"\']*)["\']',
    ]
    for pat in patterns:
        for value in re.findall(pat,text,flags=re.I):
            if len(value)>600 or value.startswith(("javascript:","data:")): continue
            url=absolute(base,value)
            if "kbsavings.com" in url: out.add(url)
    return sorted(out)

def rate_contexts(text):
    out=[]
    for word in ["금리","이율","적용이율","약정이율","기간별"]:
        for ctx in contexts(text,word,800,20):
            if any(x in ctx for x in ["3개월","6개월","12개월","24개월","36개월","ISA","퇴직연금","IRP"]):
                out.append({"keyword":word,"context":ctx})
    return out

def safe_name(url,idx):
    p=urllib.parse.urlparse(url); name=Path(p.path).name or "index"
    if p.query: name += "_" + re.sub(r"[^A-Za-z0-9._-]+","_",p.query)[:70]
    return f"{idx:03d}_"+re.sub(r"[^A-Za-z0-9._-]+","_",name)

def inspect(url):
    r=fetch(url)
    return {"url":r["url"],"status":r["status"],"content_type":r["type"],"size":len(r["raw"]),
            "target_hits":target_hits(r["text"]),"identifiers":extract_identifiers(r["text"]),
            "endpoints":extract_endpoints(r["text"],r["url"]),"links":extract_links(r["text"],r["url"]),
            "rate_contexts":rate_contexts(r["text"]),"_raw":r["raw"]}

def score(item):
    s=0; h=item.get("target_hits",{})
    if "ISA정기예금" in h: s+=20
    elif "ISA" in h: s+=5
    if "퇴직연금 정기예금" in h: s+=20
    elif "퇴직연금" in h: s+=10
    if "IRP" in h: s+=5
    if "DC형" in h: s+=3
    if item.get("identifiers"): s+=5
    if item.get("rate_contexts"): s+=5
    return s

def main():
    print("="*84); print("SBRateBot V5 KB Savings Mobile ISA / IRP Probe v5"); print("="*84)
    CACHE.mkdir(parents=True,exist_ok=True)
    queue=list(SEEDS); seen=set(); pages=[]; errors=[]; max_pages=70
    while queue and len(seen)<max_pages:
        url=queue.pop(0)
        if url in seen: continue
        seen.add(url)
        try:
            item=inspect(url); sc=score(item)
            print(f"[{len(seen):02d}] score={sc:02d} {item['status']} {item['size']:,}B {item['url']}")
            cache=CACHE/safe_name(item["url"],len(seen)); cache.write_bytes(item["_raw"])
            item["cache_file"]=str(cache); item.pop("_raw"); pages.append(item)
            for nxt in sorted(set(item["links"]+item["endpoints"])):
                low=nxt.lower()
                if "kbsavings.com" not in nxt or "/mobweb/" not in low: continue
                if not any(k in low for k in ("saving","deposit","prod","prd","goods","gds","pension","retire","isa","irp","customer")): continue
                if nxt not in seen and nxt not in queue: queue.append(nxt)
        except Exception as e:
            print("     FAIL:",e); errors.append({"url":url,"error":repr(e)})

    focused=[x for x in pages if score(x)>0]
    focused.sort(key=score,reverse=True)
    identifiers=[]; endpoints=set()
    for item in focused:
        for ident in item.get("identifiers",[]): identifiers.append({"source":item["url"],**ident})
        endpoints.update(item.get("endpoints",[]))
    result={"seeds":SEEDS,"focused_pages":focused,"all_identifiers":identifiers,
            "all_endpoints":sorted(endpoints),"errors":errors}
    OUT_JSON.parent.mkdir(parents=True,exist_ok=True)
    OUT_JSON.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")

    lines=["="*100,"SBRateBot V5 KB Savings Mobile ISA / IRP Probe v5","="*100,""]
    for item in focused:
        lines += ["-"*100,f"SCORE={score(item)}",item["url"],"-"*100]
        for kw,ctxs in item.get("target_hits",{}).items():
            lines.append("[TARGET] "+kw)
            for ctx in ctxs[:10]: lines.append("  "+ctx[:2400])
        if item.get("identifiers"):
            lines.append("[IDENTIFIERS]")
            for ident in item["identifiers"][:80]:
                lines.append(f"  {ident['type']} = {ident['value']}")
                lines.append("    "+ident["context"][:1800])
        if item.get("rate_contexts"):
            lines.append("[RATE CONTEXTS]")
            for rc in item["rate_contexts"][:60]: lines.append(f"  ({rc['keyword']}) "+rc["context"][:2200])
        if item.get("endpoints"):
            lines.append("[ENDPOINTS]")
            for ep in item["endpoints"][:150]: lines.append("  "+ep)
        lines.append("")
    lines += ["="*100,"ALL IDENTIFIERS","="*100]
    for x in identifiers:
        lines.append(f"{x['type']}={x['value']} | {x['source']}")
        lines.append("  "+x["context"][:1400])
    lines += ["","="*100,"ALL ENDPOINTS","="*100] + sorted(endpoints)
    OUT_TXT.write_text("\n".join(lines),encoding="utf-8")

    print("\n"+"="*84); print("탐색 완료"); print("="*84)
    print("Focused pages :",len(focused)); print("Identifiers   :",len(identifiers)); print("Endpoints     :",len(endpoints))
    print("JSON:",OUT_JSON); print("TXT :",OUT_TXT)
    print("※ KB저축은행 모바일 ISA/IRP 탐색 전용 / 실제 금리 JSON 미수정")

if __name__=="__main__":
    main()
