# SBRateBot V5 - KB ISA / IRP Official Page Probe v1
import json, re, ssl, urllib.parse, urllib.request
from pathlib import Path

BASES=["https://mbkt.kbsavings.com","https://m.kbsavings.com","https://mbkd.kbsavings.com"]
SEEDS=["/mobweb/main.do","/mobweb/kiwicustomer/prt_fnce_prd_regt.do"]
KEYWORDS=["ISA정기예금","ISA","퇴직연금 정기예금","퇴직연금","IRP","DC형"]
OUT_JSON=Path("data/kb_isa_irp_probe_v1.json")
OUT_TXT=Path("data/kb_isa_irp_probe_v1.txt")
CTX=ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE

def fetch(url,timeout=30):
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 Chrome/142","Accept":"text/html,application/xhtml+xml,application/json,*/*"})
    with urllib.request.urlopen(req,timeout=timeout,context=CTX) as r:
        raw=r.read()
        charset=r.headers.get_content_charset() or "utf-8"
        return {"url":r.geturl(),"status":r.status,"content_type":r.headers.get("Content-Type",""),"text":raw.decode(charset,errors="replace")}

def links(html,base):
    out=set()
    for pat in [r'href\s*=\s*["\\\']([^"\\\']+)["\\\']',r'action\s*=\s*["\\\']([^"\\\']+)["\\\']',r'src\s*=\s*["\\\']([^"\\\']+)["\\\']']:
        for x in re.findall(pat,html,flags=re.I):
            if not x.startswith(("javascript:","#","mailto:")):
                out.add(urllib.parse.urljoin(base,x))
    return sorted(out)

def candidates(text,base):
    out=set()
    for x in re.findall(r'["\\\']([^"\\\']+\.(?:do|json|ajax)(?:\?[^"\\\']*)?)["\\\']',text,flags=re.I):
        out.add(urllib.parse.urljoin(base,x))
    return sorted(out)

def contexts(text,kw,radius=350):
    ans=[]; low=text.lower(); key=kw.lower(); pos=0
    while True:
        i=low.find(key,pos)
        if i<0: break
        ans.append(text[max(0,i-radius):min(len(text),i+len(kw)+radius)].replace("\n"," "))
        pos=i+len(kw)
    return ans[:20]

def main():
    print("="*78); print("SBRateBot V5 KB ISA / IRP Official Page Probe v1"); print("="*78)
    result={"targets":{},"pages":[],"errors":[]}
    queue=[b+s for b in BASES for s in SEEDS]; seen=set()

    while queue and len(seen)<30:
        url=queue.pop(0)
        if url in seen: continue
        seen.add(url)
        try:
            r=fetch(url); text=r["text"]
            print(f"[{len(seen):02d}] {url}"); print(f"     HTTP {r['status']} / {len(text):,} chars")
            hits={}
            for kw in KEYWORDS:
                c=contexts(text,kw)
                if c: hits[kw]=c
            result["pages"].append({"requested_url":url,"final_url":r["url"],"status":r["status"],"content_type":r["content_type"],"keyword_hits":hits,"candidates":candidates(text,r["url"])})
            for link in links(text,r["url"]):
                if "kbsavings.com" in link and any(x in link.lower() for x in ("saving","deposit","prod","goods","pension","retire","isa","irp","customer","prd")):
                    if link not in seen and link not in queue: queue.append(link)
        except Exception as e:
            print("     FAIL:",e); result["errors"].append({"url":url,"error":repr(e)})

    for target,kws in {"ISA":["ISA정기예금","ISA"],"IRP":["퇴직연금 정기예금","퇴직연금","IRP","DC형"]}.items():
        matches=[]
        for p in result["pages"]:
            score=sum(len(p["keyword_hits"].get(k,[])) for k in kws)
            if score: matches.append({"score":score,"url":p["final_url"],"keyword_hits":p["keyword_hits"],"candidates":p["candidates"]})
        result["targets"][target]=sorted(matches,key=lambda x:-x["score"])

    OUT_JSON.parent.mkdir(parents=True,exist_ok=True)
    OUT_JSON.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    report=["="*90,"SBRateBot V5 KB ISA / IRP Probe v1","="*90]
    for target in ("ISA","IRP"):
        report += ["","-"*90,target,"-"*90]
        for i,m in enumerate(result["targets"][target][:10],1):
            report.append(f"[{i}] score={m['score']} {m['url']}")
            for kw,ctxs in m["keyword_hits"].items():
                report.append("  KEYWORD: "+kw)
                for ctx in ctxs[:5]: report.append("    "+ctx[:1200])
            if m["candidates"]:
                report.append("  URL/API candidates:")
                report += ["    "+c for c in m["candidates"][:50]]
    OUT_TXT.write_text("\n".join(report),encoding="utf-8")
    print("\n탐색 완료"); print("JSON:",OUT_JSON); print("TXT :",OUT_TXT)
    print("※ 데이터 파일은 수정하지 않습니다.")

if __name__=="__main__":
    main()
