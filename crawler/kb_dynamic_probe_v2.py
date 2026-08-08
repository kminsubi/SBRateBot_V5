# SBRateBot V5 - KB Savings Dynamic Rate Probe v2
import json, re, ssl, urllib.parse, urllib.request
from pathlib import Path

ENTRY="https://www.kbsavings.com/?conn_gb=690"
OUT_JSON=Path("data/kb_dynamic_probe_v2.json")
OUT_TXT=Path("data/kb_dynamic_probe_v2.txt")
CACHE=Path("data/kb_dynamic_probe_cache")
KEYWORDS=["ISA정기예금","ISA","퇴직연금 정기예금","퇴직연금","IRP","DC형","DC/IRP","금리","이율","적용이율","3개월","6개월","12개월","24개월","36개월"]
CTX=ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE

def fetch(url,timeout=60):
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/142 Safari/537.36","Accept":"*/*","Referer":"https://www.kbsavings.com/"})
    with urllib.request.urlopen(req,timeout=timeout,context=CTX) as r:
        raw=r.read(); charset=r.headers.get_content_charset() or "utf-8"
        return {"url":r.geturl(),"status":r.status,"type":r.headers.get("Content-Type",""),"raw":raw,"text":raw.decode(charset,errors="replace")}

def assets(html,base):
    out=set()
    for pat in [r'<script[^>]+src=["\']([^"\']+)["\']',r'<iframe[^>]+src=["\']([^"\']+)["\']',r'<link[^>]+href=["\']([^"\']+)["\']']:
        for x in re.findall(pat,html,flags=re.I):
            if not x.startswith(("javascript:","data:","#")): out.add(urllib.parse.urljoin(base,x))
    return sorted(out)

def endpoints(text,base):
    out=set()
    pats=[r'["\']([^"\']+\.(?:do|json|ajax|jsp)(?:\?[^"\']*)?)["\']',
          r'["\']((?:/|https?://)[^"\']*(?:api|ajax|rate|interest|intr|prod|goods|saving|deposit|isa|irp|retire|pension)[^"\']*)["\']']
    for pat in pats:
        for x in re.findall(pat,text,flags=re.I):
            if len(x)<500 and not x.startswith(("javascript:","data:")): out.add(urllib.parse.urljoin(base,x))
    return sorted(out)

def contexts(text,radius=500):
    out={}
    for kw in KEYWORDS:
        low=text.lower(); key=kw.lower(); pos=0; vals=[]
        while True:
            i=low.find(key,pos)
            if i<0: break
            vals.append(text[max(0,i-radius):min(len(text),i+len(kw)+radius)].replace("\r"," ").replace("\n"," "))
            pos=i+len(kw)
            if len(vals)>=15: break
        if vals: out[kw]=vals
    return out

def rate_candidates(text):
    out=[]
    pats=[r'(?P<term>3|6|12|24|36)\s*개월.{0,100}?(?P<rate>\d+(?:\.\d+)?)\s*%',
          r'(?P<rate>\d+(?:\.\d+)?)\s*%.{0,100}?(?P<term>3|6|12|24|36)\s*개월']
    for pat in pats:
        for m in re.finditer(pat,text,flags=re.I|re.S):
            out.append({"term":m.group("term")+"m","rate":float(m.group("rate")),
                        "context":text[max(0,m.start()-200):min(len(text),m.end()+200)].replace("\n"," ")})
    return out

def safe_name(url,i):
    name=Path(urllib.parse.urlparse(url).path).name or "index"
    return f"{i:03d}_"+re.sub(r"[^A-Za-z0-9._-]+","_",name)

def inspect_item(r):
    return {"url":r["url"],"content_type":r["type"],"size":len(r["raw"]),
            "keyword_contexts":contexts(r["text"]),
            "endpoint_candidates":endpoints(r["text"],r["url"]),
            "rate_candidates":rate_candidates(r["text"])}

def main():
    print("="*80); print("SBRateBot V5 KB Savings Dynamic Rate Probe v2"); print("="*80)
    CACHE.mkdir(parents=True,exist_ok=True)
    result={"entry":ENTRY,"pages":[],"assets":[],"all_endpoint_candidates":[],"all_rate_candidates":[],"errors":[]}
    print("[1] KB저축은행 진입 페이지")
    root=fetch(ENTRY); print("    HTTP:",root["status"]); print("    FINAL:",root["url"]); print("    SIZE:",len(root["raw"]))
    result["pages"].append(inspect_item(root))
    urls=[u for u in assets(root["text"],root["url"]) if ".js" in u.lower() or "iframe" in u.lower() or ".do" in u.lower() or ".jsp" in u.lower() or "kbsavings.com" in u.lower()][:100]
    print("[2] asset/iframe 후보:",len(urls))
    for i,url in enumerate(urls,1):
        print(f"    [{i}/{len(urls)}] {url}")
        try:
            r=fetch(url,90); f=CACHE/safe_name(url,i); f.write_bytes(r["raw"])
            item=inspect_item(r); item["cache_file"]=str(f); result["assets"].append(item)
        except Exception as e:
            print("       FAIL:",e); result["errors"].append({"url":url,"error":repr(e)})
    eps=set(); rates=[]
    for item in result["pages"]+result["assets"]:
        eps.update(item.get("endpoint_candidates",[]))
        for x in item.get("rate_candidates",[]): rates.append({"source":item["url"],**x})
    result["all_endpoint_candidates"]=sorted(eps); result["all_rate_candidates"]=rates
    OUT_JSON.parent.mkdir(parents=True,exist_ok=True)
    OUT_JSON.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    lines=["="*100,"SBRateBot V5 KB Savings Dynamic Rate Probe v2","="*100,"","ENTRY: "+ENTRY,""]
    for item in result["pages"]+result["assets"]:
        if not item.get("keyword_contexts") and not item.get("rate_candidates"): continue
        lines += ["-"*100,item["url"],"-"*100]
        for kw,ctxs in item["keyword_contexts"].items():
            lines.append("[KEYWORD] "+kw)
            for ctx in ctxs[:8]: lines.append("  "+ctx[:1800])
        if item["rate_candidates"]:
            lines.append("[RATE CANDIDATES]")
            for x in item["rate_candidates"]:
                lines.append(f"  {x['term']} = {x['rate']}%"); lines.append("    "+x["context"][:1200])
        if item["endpoint_candidates"]:
            lines.append("[ENDPOINT CANDIDATES]"); lines += ["  "+x for x in item["endpoint_candidates"][:100]]
        lines.append("")
    lines += ["="*100,"ALL ENDPOINT CANDIDATES","="*100] + result["all_endpoint_candidates"]
    lines += ["","="*100,"ALL RATE CANDIDATES","="*100]
    for x in rates:
        lines.append(f"{x['term']} = {x['rate']}% | {x['source']}"); lines.append("  "+x["context"][:1000])
    OUT_TXT.write_text("\n".join(lines),encoding="utf-8")
    print("\n탐색 완료"); print("JSON :",OUT_JSON); print("TXT  :",OUT_TXT); print("CACHE:",CACHE)
    print("※ KB저축은행 www.kbsavings.com 기준이며 실제 금리 JSON은 수정하지 않습니다.")

if __name__=="__main__":
    main()
