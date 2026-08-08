# -*- coding: utf-8 -*-
import json, re, time
from collections import deque
from pathlib import Path
from urllib.parse import urljoin, urlparse
import requests

BASE="https://sb.koreainvestment.com"
START={"ISA":BASE+"/?PRD-PDS001-10#","IRP":BASE+"/?PRD-PDS001-11#"}
OUT=Path("data"); OUT.mkdir(exist_ok=True)
REPORT=OUT/"koreainvest_rate_probe_v3.txt"
RESULT=OUT/"koreainvest_rate_candidates_v3.json"
S=requests.Session()
S.headers.update({"User-Agent":"Mozilla/5.0","Accept-Language":"ko-KR,ko;q=0.9","Referer":BASE+"/"})

def norm(x,parent=BASE+"/"):
    if not x:return None
    x=x.strip().strip(chr(34)).strip(chr(39)).replace("&amp;","&")
    if x.startswith(("#","javascript:","data:","mailto:","tel:")):return None
    u=urljoin(parent,x)
    return u.split("#")[0] if urlparse(u).netloc==urlparse(BASE).netloc else None

def get(u):
    try:
        r=S.get(u,timeout=15,allow_redirects=True)
        r.encoding=r.apparent_encoding or r.encoding or "utf-8"
        return r,r.text
    except Exception:return None,""

def extract_urls(t,parent):
    out=set()
    patterns=[
        r"(?:src|href|url|action|ref|w2xPath|contentUrl)\s*[:=]\s*[\"']([^\"'<>]+)[\"']",
        r"[\"']([^\"']+\.(?:xml|js|do)(?:\?[^\"']*)?)[\"']",
        r"[\"']([^\"']*(?:PRD|PDS|prd|pds)[^\"']*)[\"']"
    ]
    for p in patterns:
        for x in re.findall(p,t,re.I):
            u=norm(x,parent)
            if u:out.add(u)
    return out

def snippets(t,key,radius=800,limit=12):
    low=t.lower(); k=key.lower(); pos=0; out=[]
    while len(out)<limit:
        i=low.find(k,pos)
        if i<0:break
        out.append((i,t[max(0,i-radius):min(len(t),i+len(key)+radius)].replace("\r","")))
        pos=i+len(k)
    return out

def endpoints(t,parent):
    out=set()
    for x in re.findall(r"[\"']([^\"']+\.do(?:\?[^\"']*)?)[\"']",t,re.I):
        u=norm(x,parent)
        if u:out.add(u)
    return out

def score(t,u=""):
    x=(t+"\n"+u).lower(); n=0
    for k,w in [("prd-pds001-10",100),("prd-pds001-11",100),("intrgridview",90),
                ("금리안내",80),("적용금리",70),("금리",45),("submission",35),
                (".do",30),("w2xpath",25),("contenturl",25),("rate",10),("intr",8)]:
        if k in x:n+=w
    return n

def main():
    q=deque(); seen=set(); discovered=set(); api=[]; xml=set()
    result={"ISA":[],"IRP":[],"api":[],"xml":[]}
    seeds=["/websquare/config.xml","/websquare/configPcw.js","/websquare/javascript.wq?q=/bootloader",
           "/assets/js/com/commonGlobal.js","/assets/js/com/commonScope.js",
           "/assets/p/js/common.js","/assets/lcst/js/common.js"]
    with REPORT.open("w",encoding="utf-8") as f:
        def sec(x):f.write("\n"+"="*110+"\n"+x+"\n"+"="*110+"\n")
        sec("SBRateBot V5 한국투자저축은행 WebSquare Route Probe v3")
        f.write("ISA = PRD-PDS001-10\nIRP = PRD-PDS001-11\n")
        f.write("목표 = 메뉴 ID -> 실제 XML/w2xPath -> 금리안내 -> submission/API 역추적\n")
        for label,u in START.items():
            r,t=get(u); sec(label+" INITIAL")
            if not r:continue
            f.write(f"URL={u}\nFINAL={r.url}\nHTTP={r.status_code}\nSIZE={len(t)}\n")
            for v in extract_urls(t,r.url):
                if v not in discovered:discovered.add(v);q.append(v)
        for x in seeds:
            u=norm(x)
            if u not in discovered:discovered.add(u);q.append(u)
        sec("RECURSIVE ROUTE / XML / API TRACE")
        no=0
        while q and len(seen)<180:
            u=q.popleft()
            if u in seen:continue
            seen.add(u);r,t=get(u)
            if not r or not t:continue
            ct=(r.headers.get("Content-Type") or "").lower()
            if not any(z in ct for z in ("text","javascript","json","xml")) and not re.search(r"\.(js|xml|html|css)(\?|$)",r.url,re.I):continue
            no+=1
            for v in extract_urls(t,r.url):
                if v not in discovered and v not in seen:discovered.add(v);q.append(v)
                if ".xml" in v.lower():xml.add(v)
            eps=endpoints(t,r.url)
            for ep in eps:api.append({"url":ep,"source":r.url})
            menu_hit=False
            for label,mid in [("ISA","PRD-PDS001-10"),("IRP","PRD-PDS001-11")]:
                hs=snippets(t,mid,1100,20)
                if hs:
                    menu_hit=True;sec(f"MENU ROUTE HIT - {label} - RESOURCE #{no}");f.write("URL="+r.url+"\n")
                    for p,snip in hs:
                        f.write(f"\n>>> {mid} @{p}\n{snip}\n")
                        result[label].append({"source":r.url,"position":p,"snippet":snip})
                        for v in extract_urls(snip,r.url):
                            if ".xml" in v.lower():
                                xml.add(v)
                                if v not in discovered and v not in seen:discovered.add(v);q.appendleft(v)
            sc=score(t,r.url)
            if sc>=45 or menu_hit or eps:
                sec(f"INTERESTING RESOURCE #{no}")
                f.write(f"URL={r.url}\nHTTP={r.status_code}\nSIZE={len(t)}\nSCORE={sc}\n")
                for k in ["intrGridView","금리안내","금리","submission","w2xPath","contentUrl",".do"]:
                    hs=snippets(t,k,600,6)
                    if hs:
                        f.write(f"\n>>> HIT [{k}] count={len(hs)}\n")
                        for p,snip in hs:f.write(f"\n--- @{p} ---\n{snip}\n")
                if eps:
                    f.write("\n>>> .do/API ENDPOINTS\n")
                    for ep in sorted(eps):f.write(ep+"\n")
            time.sleep(.05)
        sec("XML CANDIDATE DIRECT PROBE")
        for i,u in enumerate(sorted(xml)[:100],1):
            r,t=get(u)
            if not r or not t:continue
            if score(t,r.url)<20 and not any(x in t.lower() for x in ("submission","intrgridview","금리안내",".do")):continue
            f.write(f"\n[XML {i}] {r.url}\nHTTP={r.status_code} SIZE={len(t)} SCORE={score(t,r.url)}\n")
            for k in ["PRD-PDS001-10","PRD-PDS001-11","intrGridView","금리안내","금리","submission",".do"]:
                for p,snip in snippets(t,k,700,8):f.write(f"\n>>> {k} @{p}\n{snip}\n")
            for ep in endpoints(t,r.url):api.append({"url":ep,"source":r.url})
        uniq={}
        for x in api:uniq.setdefault(x["url"],x)
        api=list(uniq.values())
        for x in api:
            low=x["url"].lower()
            x["score"]=sum(w for k,w in [("prd",20),("pds",20),("dps",20),("intr",35),
                                         ("rate",30),("inrst",30),("interest",30),("deposit",20)] if k in low)
        api.sort(key=lambda x:x["score"],reverse=True)
        result["api"]=api;result["xml"]=sorted(xml)
        sec("FINAL SUMMARY")
        f.write(f"VISITED_RESOURCES={len(seen)}\nDISCOVERED_RESOURCES={len(discovered)}\n")
        f.write(f"ISA_ROUTE_HITS={len(result['ISA'])}\nIRP_ROUTE_HITS={len(result['IRP'])}\n")
        f.write(f"XML_CANDIDATES={len(xml)}\nAPI_CANDIDATES={len(api)}\n\nTOP API CANDIDATES\n")
        for x in api[:30]:f.write(f"[score={x['score']:03d}] {x['url']}\n    source={x['source']}\n")
        f.write("\n보낼 부분: MENU ROUTE HIT / XML CANDIDATE DIRECT PROBE / FINAL SUMMARY / TOP API CANDIDATES\n")
    with RESULT.open("w",encoding="utf-8") as f:json.dump(result,f,ensure_ascii=False,indent=2)
    print("REPORT :",REPORT);print("JSON :",RESULT)
    print("실행 후 MENU ROUTE HIT / XML CANDIDATE DIRECT PROBE / FINAL SUMMARY를 보내주세요.")
if __name__=="__main__":main()
