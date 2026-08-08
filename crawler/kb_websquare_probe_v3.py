# SBRateBot V5 - KB Savings WebSquare Probe v3
import json, re, ssl, urllib.parse, urllib.request
from pathlib import Path

BASE="https://www.kbsavings.com"
START=BASE+"/websquare/websquare.jsp?w2xPath=/jsp/main.xml"
OUT_JSON=Path("data/kb_websquare_probe_v3.json")
OUT_TXT=Path("data/kb_websquare_probe_v3.txt")
CACHE=Path("data/kb_websquare_probe_cache")
KEYWORDS=["ISA정기예금","ISA","퇴직연금 정기예금","퇴직연금","IRP","DC형","DC/IRP","금리","이율","적용이율","3개월","6개월","12개월","24개월","36개월"]
CTX=ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE

def fetch(url,timeout=60):
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 Chrome/142","Accept":"*/*","Referer":BASE+"/"})
    with urllib.request.urlopen(req,timeout=timeout,context=CTX) as r:
        raw=r.read(); charset=r.headers.get_content_charset() or "utf-8"
        return {"url":r.geturl(),"status":r.status,"type":r.headers.get("Content-Type",""),"raw":raw,"text":raw.decode(charset,errors="replace")}

def abs_url(base,val):
    return urllib.parse.urljoin(base,val)

def safe_name(url,i):
    p=urllib.parse.urlparse(url); name=Path(p.path).name or "index"
    if p.query: name += "_" + re.sub(r"[^A-Za-z0-9._-]+","_",p.query)[:60]
    return f"{i:03d}_"+re.sub(r"[^A-Za-z0-9._-]+","_",name)

def contexts(text,radius=600):
    out={}; low=text.lower()
    for kw in KEYWORDS:
        vals=[]; pos=0; key=kw.lower()
        while True:
            idx=low.find(key,pos)
            if idx<0: break
            vals.append(text[max(0,idx-radius):min(len(text),idx+len(kw)+radius)].replace("\r"," ").replace("\n"," "))
            pos=idx+len(kw)
            if len(vals)>=20: break
        if vals: out[kw]=vals
    return out

def extract_paths(text,base):
    out=set()
    patterns=[
        r'''["\']([^"\']+\.xml(?:\?[^"\']*)?)["\']''',
        r'''["\']([^"\']+\.jsp(?:\?[^"\']*)?)["\']''',
        r'''["\']([^"\']+\.do(?:\?[^"\']*)?)["\']''',
        r'''["\']([^"\']+\.json(?:\?[^"\']*)?)["\']'''
    ]
    for pat in patterns:
        for v in re.findall(pat,text,flags=re.I):
            if not v.startswith(("javascript:","data:")):
                out.add(abs_url(base,v))
    return sorted(out)

def websquare_refs(text,base):
    out=set()
    for v in re.findall(r'w2xPath=([^"\'&\s]+\.xml)',text,flags=re.I):
        dec=urllib.parse.unquote(v)
        out.add(BASE+"/websquare/websquare.jsp?w2xPath="+dec)
        out.add(abs_url(BASE+"/",dec))
    return sorted(out)

def submission_contexts(text):
    out=[]; low=text.lower()
    for key in ["submission","action=","service","url=",".do",".json"]:
        pos=0
        while True:
            idx=low.find(key.lower(),pos)
            if idx<0: break
            out.append({"keyword":key,"context":text[max(0,idx-450):min(len(text),idx+1000)].replace("\r"," ").replace("\n"," ")})
            pos=idx+len(key)
            if len(out)>=200: return out
    return out

def rate_candidates(text):
    out=[]
    pats=[
        r'(?P<term>3|6|12|24|36)\s*개월.{0,120}?(?P<rate>\d+(?:\.\d+)?)\s*%',
        r'(?P<rate>\d+(?:\.\d+)?)\s*%.{0,120}?(?P<term>3|6|12|24|36)\s*개월'
    ]
    for pat in pats:
        for m in re.finditer(pat,text,flags=re.I|re.S):
            out.append({"term":m.group("term")+"m","rate":float(m.group("rate")),"context":text[max(0,m.start()-250):min(len(text),m.end()+250)].replace("\n"," ")})
    return out

def inspect(url):
    r=fetch(url)
    return {
        "url":r["url"],"status":r["status"],"content_type":r["type"],"size":len(r["raw"]),
        "keyword_contexts":contexts(r["text"]),
        "path_candidates":extract_paths(r["text"],r["url"]),
        "websquare_refs":websquare_refs(r["text"],r["url"]),
        "submission_like":submission_contexts(r["text"]),
        "rate_candidates":rate_candidates(r["text"]),
        "_raw":r["raw"]
    }

def main():
    print("="*84); print("SBRateBot V5 KB Savings WebSquare Probe v3"); print("="*84)
    CACHE.mkdir(parents=True,exist_ok=True)
    result={"start":START,"pages":[],"errors":[]}
    queue=[START]; seen=set(); max_pages=60
    while queue and len(seen)<max_pages:
        url=queue.pop(0)
        if url in seen: continue
        seen.add(url)
        try:
            item=inspect(url)
            print(f"[{len(seen):02d}] {item['status']} {item['size']:,}B {item['url']}")
            cache=CACHE/safe_name(item["url"],len(seen)); cache.write_bytes(item["_raw"])
            item["cache_file"]=str(cache); item.pop("_raw")
            result["pages"].append(item)
            for nxt in sorted(set(item["path_candidates"]+item["websquare_refs"])):
                if "kbsavings.com" in nxt and any(x in nxt.lower() for x in (".xml","websquare.jsp",".do",".jsp")):
                    if nxt not in seen and nxt not in queue: queue.append(nxt)
        except Exception as e:
            print("     FAIL:",e); result["errors"].append({"url":url,"error":repr(e)})
    all_paths=sorted({p for item in result["pages"] for p in item.get("path_candidates",[])})
    all_refs=sorted({p for item in result["pages"] for p in item.get("websquare_refs",[])})
    rates=[]
    for item in result["pages"]:
        for x in item.get("rate_candidates",[]): rates.append({"source":item["url"],**x})
    result["all_paths"]=all_paths; result["all_websquare_refs"]=all_refs; result["all_rate_candidates"]=rates
    OUT_JSON.parent.mkdir(parents=True,exist_ok=True)
    OUT_JSON.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    lines=["="*100,"SBRateBot V5 KB Savings WebSquare Probe v3","="*100,"","START: "+START,""]
    for item in result["pages"]:
        if not item.get("keyword_contexts") and not item.get("rate_candidates") and not item.get("submission_like"): continue
        lines += ["-"*100,item["url"],"-"*100]
        for kw,ctxs in item.get("keyword_contexts",{}).items():
            lines.append("[KEYWORD] "+kw)
            for c in ctxs[:10]: lines.append("  "+c[:2200])
        if item.get("rate_candidates"):
            lines.append("[RATE CANDIDATES]")
            for x in item["rate_candidates"]:
                lines.append(f"  {x['term']} = {x['rate']}%"); lines.append("    "+x["context"][:1500])
        if item.get("path_candidates"):
            lines.append("[PATH CANDIDATES]"); lines += ["  "+x for x in item["path_candidates"][:120]]
        if item.get("websquare_refs"):
            lines.append("[WEBSQUARE REFS]"); lines += ["  "+x for x in item["websquare_refs"][:120]]
        if item.get("submission_like"):
            lines.append("[SUBMISSION/SERVICE CONTEXTS]")
            for s in item["submission_like"][:80]: lines.append(f"  ({s['keyword']}) "+s["context"][:1800])
        lines.append("")
    lines += ["="*100,"ALL PATHS","="*100] + all_paths
    lines += ["","="*100,"ALL WEBSQUARE REFS","="*100] + all_refs
    lines += ["","="*100,"ALL RATE CANDIDATES","="*100]
    for x in rates:
        lines.append(f"{x['term']} = {x['rate']}% | {x['source']}"); lines.append("  "+x["context"][:1200])
    OUT_TXT.write_text("\n".join(lines),encoding="utf-8")
    print("\n탐색 완료"); print("JSON :",OUT_JSON); print("TXT  :",OUT_TXT); print("CACHE:",CACHE)
    print("※ KB저축은행 WebSquare 분석 전용 / 실제 금리 JSON 미수정")

if __name__=="__main__":
    main()
