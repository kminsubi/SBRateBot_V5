# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path
from urllib.parse import urljoin
import requests

BASE="https://sb.koreainvestment.com"
TARGETS={
    "ISA":BASE+"/?PRD-PDS001-10#",
    "IRP":BASE+"/?PRD-PDS001-11#",
}
OUT_JSON=Path("data/koreainvest_rate_probe_v1.json")
OUT_TXT=Path("data/koreainvest_rate_probe_v1.txt")

KEYWORDS=[
    "PRD-PDS001-10","PRD-PDS001-11","금리안내","금리","이율",
    "interest","rate","ISA","퇴직연금","IRP","ajax","fetch(",
    "$.ajax","axios",".do",".json","api","product","prd"
]

S=requests.Session()
S.headers.update({
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/142.0 Safari/537.36",
    "Accept-Language":"ko-KR,ko;q=0.9,en;q=0.8",
})

def fetch(url,referer=None):
    h={}
    if referer:h["Referer"]=referer
    r=S.get(url,headers=h,timeout=40,allow_redirects=True)
    if not r.encoding or r.encoding.lower()=="iso-8859-1":
        r.encoding=r.apparent_encoding or "utf-8"
    return r

def context(text,pos,before=1800,after=3500):
    return text[max(0,pos-before):min(len(text),pos+after)]

def collect_hits(text):
    low=text.lower()
    hits=[]
    for keyword in KEYWORDS:
        start=0
        while True:
            pos=low.find(keyword.lower(),start)
            if pos<0:break
            hits.append({"keyword":keyword,"position":pos,"context":context(text,pos)})
            start=pos+max(1,len(keyword))
            if len(hits)>=300:break
    hits.sort(key=lambda x:x["position"])
    result=[]
    last=-100000
    for item in hits:
        if item["position"]-last<250:continue
        result.append(item);last=item["position"]
    return result[:120]

def extract_resources(text,base_url):
    found=set()
    patterns=[
        r'(?:src|href)\s*=\s*["\x27]([^"\x27]+)["\x27]',
        r'["\x27]([^"\x27]+\.(?:js|json|html|jsp|do|xml)(?:\?[^"\x27]*)?)["\x27]'
    ]
    for pattern in patterns:
        for m in re.finditer(pattern,text,flags=re.I):
            value=m.group(1).strip()
            if not value or value.startswith(("javascript:","mailto:","tel:","#","data:")):
                continue
            url=urljoin(base_url,value)
            if "sb.koreainvestment.com" in url:
                found.add(url)
    return sorted(found)

def score(text,url=""):
    low=text.lower()
    weights={
        "prd-pds001-10":150,"prd-pds001-11":150,"금리안내":100,
        "금리":50,"이율":50,"isa":40,"퇴직연금":60,"irp":40,
        "interest":25,"rate":20,"ajax":20,".do":20,".json":20,"api":15
    }
    s=sum(min(low.count(k),20)*v for k,v in weights.items())
    if "prd" in url.lower():s+=50
    return s

def main():
    print("="*92)
    print("SBRateBot V5 - 한국투자저축은행 금리안내 Probe v1")
    print("="*92)
    result={"bank":"한국투자","targets":TARGETS,"pages":{},"resources":[]}
    resources=set()

    for kind,url in TARGETS.items():
        print("\n[PAGE]",kind,url)
        try:
            r=fetch(url)
            print("HTTP:",r.status_code,"SIZE:",len(r.content),"FINAL:",r.url)
            result["pages"][kind]={
                "url":url,"final_url":r.url,"status":r.status_code,
                "content_type":r.headers.get("Content-Type"),"size":len(r.content),
                "cookies":S.cookies.get_dict(),"hits":collect_hits(r.text),
                "text":r.text[:400000]
            }
            resources.update(extract_resources(r.text,r.url))
        except Exception as e:
            print("ERROR:",repr(e))
            result["pages"][kind]={"url":url,"error":repr(e)}

    candidates=list(resources)[:160]
    print("\n[RESOURCES]",len(candidates))
    inspected=[]

    for idx,url in enumerate(candidates,1):
        low_url=url.lower()
        if low_url.endswith((".png",".jpg",".jpeg",".gif",".svg",".ico",".woff",".woff2",".ttf",".css")):
            continue
        try:
            r=fetch(url,TARGETS["ISA"])
            text=r.text
            s=score(text,r.url)
            if s<=0:continue
            item={
                "url":r.url,"status":r.status_code,
                "content_type":r.headers.get("Content-Type"),
                "size":len(r.content),"score":s,
                "hits":collect_hits(text),"text":text[:350000]
            }
            inspected.append(item)
            print(f"[{idx}] HTTP {r.status_code} SCORE {s} {r.url}")
        except Exception as e:
            if "prd" in low_url or ".js" in low_url:
                inspected.append({"url":url,"error":repr(e)})

    inspected.sort(key=lambda x:x.get("score",0),reverse=True)
    result["resources"]=inspected
    OUT_JSON.parent.mkdir(parents=True,exist_ok=True)
    OUT_JSON.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")

    lines=[
        "="*120,"SBRateBot V5 한국투자저축은행 ISA / 퇴직연금 금리안내 Probe v1",
        "="*120,"","ISA : PRD-PDS001-10","IRP : PRD-PDS001-11",""
    ]
    for kind in ("ISA","IRP"):
        page=result["pages"].get(kind,{})
        lines += [
            "="*120,f"{kind} PAGE","="*120,
            f"URL={page.get('url')}",f"FINAL={page.get('final_url')}",
            f"HTTP={page.get('status')}",f"SIZE={page.get('size')}",""
        ]
        if page.get("error"):
            lines.append("ERROR="+page["error"]);continue
        for hit in page.get("hits",[])[:80]:
            lines += ["",f">>> HIT {hit['keyword']} @ {hit['position']}",hit["context"]]

    lines += ["","="*120,"LINKED RESOURCE EVIDENCE","="*120]
    for i,item in enumerate(inspected,1):
        lines += [
            "","-"*120,f"RESOURCE #{i}",f"URL={item.get('url')}",
            f"HTTP={item.get('status')}",f"SCORE={item.get('score')}",""
        ]
        if item.get("error"):
            lines.append("ERROR="+item["error"]);continue
        for hit in item.get("hits",[])[:80]:
            lines += ["",f">>> HIT {hit['keyword']} @ {hit['position']}",hit["context"]]

    OUT_TXT.write_text("\n".join(lines),encoding="utf-8")
    print("\n완료")
    print("JSON:",OUT_JSON)
    print("TXT :",OUT_TXT)
    print("보내줄 파일: data/koreainvest_rate_probe_v1.txt")
    print("기존 ISA/IRP JSON은 수정하지 않습니다.")

if __name__=="__main__":
    main()
