import json
import re
from pathlib import Path
from urllib.parse import urljoin
import requests

BASE="https://www.idbsb.com"
PRODUCTS={
    "ISA":{"goodsCd":"C2104","menuNum":"1020"},
    "IRP":{"goodsCd":"C2103","menuNum":"1021"},
}
DETAIL_XML="/w2/itb/dps/dpstInfo.xml"
OUT_JSON=Path("data/db_websquare_probe_v1.json")
OUT_TXT=Path("data/db_websquare_probe_v1.txt")

S=requests.Session()
S.headers.update({
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/142.0 Safari/537.36",
    "Accept-Language":"ko-KR,ko;q=0.9,en;q=0.8",
})

def product_url(c):
    return (BASE+"/websquare/websquare.jsp?w2xPath=/w2/itb/main.xml"
            +"&contentUrl=/w2/itb/dps/dpstInfo.xml"
            +f"&menuNum={c['menuNum']}&goodsCtgry=C0021&goodsCd={c['goodsCd']}")

def fetch(url,referer=None):
    h={}
    if referer:h["Referer"]=referer
    r=S.get(url,headers=h,timeout=40,allow_redirects=True)
    if not r.encoding or r.encoding.lower()=="iso-8859-1":
        r.encoding=r.apparent_encoding or "utf-8"
    return r

def ctx(t,p,b=2500,a=4500):
    return t[max(0,p-b):min(len(t),p+a)]

def hits(t,keys):
    out=[]
    low=t.lower()
    for k in keys:
        st=0
        while True:
            p=low.find(k.lower(),st)
            if p<0:break
            out.append({"keyword":k,"position":p,"context":ctx(t,p)})
            st=p+max(1,len(k))
    return sorted(out,key=lambda x:x["position"])

def resources(t,base):
    out=set()
    # simple quoted resource extraction, intentionally permissive
    for m in re.finditer(r'["\']([^"\']+\.(?:xml|js)(?:\?[^"\']*)?)["\']',t,re.I):
        v=m.group(1).strip()
        if not v.startswith("javascript:"):
            out.add(urljoin(base,v))
    return sorted(out)

def score(t):
    w={"goodsCd":30,"C2104":100,"C2103":100,"dpstInfo":80,
       "transaction":30,"submission":30,"service":15,"금리":40,
       "이율":40,"interest":20,"rate":10,"ISA":30,"퇴직연금":30,"C0021":20}
    low=t.lower()
    return sum(min(low.count(k.lower()),20)*v for k,v in w.items())

def main():
    print("="*90)
    print("SBRateBot V5 DB Savings Bank WebSquare Probe v1")
    print("="*90)
    result={"base":BASE,"targets":PRODUCTS,"pages":{},"detail_xml":{},"resources":[]}
    found=set()

    for kind,cfg in PRODUCTS.items():
        u=product_url(cfg)
        print(f"\n[PAGE] {kind}: {u}")
        try:
            r=fetch(u)
            print(" HTTP",r.status_code,"SIZE",len(r.content))
            result["pages"][kind]={"url":u,"final_url":r.url,"status":r.status_code,
                                  "content_type":r.headers.get("Content-Type"),
                                  "cookies":S.cookies.get_dict(),"text_head":r.text[:15000]}
            found.update(resources(r.text,r.url))
        except Exception as e:
            print(" ERROR",e)
            result["pages"][kind]={"url":u,"error":repr(e)}

    du=urljoin(BASE,DETAIL_XML)
    print("\n[DETAIL XML]",du)
    try:
        r=fetch(du,product_url(PRODUCTS["ISA"]))
        t=r.text
        print(" HTTP",r.status_code,"SIZE",len(r.content))
        result["detail_xml"]={"url":r.url,"status":r.status_code,
            "content_type":r.headers.get("Content-Type"),"size":len(r.content),
            "text":t,"hits":hits(t,["goodsCd","goodsCtgry","dpstInfo","transaction",
            "submission","service","action","target","금리","이율","interest","rate",
            "C2104","C2103","ISA","퇴직연금"])}
        found.update(resources(t,r.url))
    except Exception as e:
        print(" ERROR",e)
        result["detail_xml"]={"url":du,"error":repr(e)}

    for p in ["/w2/itb/dps/dpstInfo.js","/w2/itb/dps/dpstInfo.xml.js","/w2/itb/main.xml"]:
        found.add(urljoin(BASE,p))

    rr=[]
    print("\n[RESOURCES]",len(found))
    for u in list(found)[:100]:
        try:
            r=fetch(u,product_url(PRODUCTS["ISA"]))
            t=r.text;s=score(t)
            if s>0 or "dpst" in u.lower() or "main.xml" in u.lower():
                item={"url":r.url,"status":r.status_code,"content_type":r.headers.get("Content-Type"),
                      "size":len(r.content),"score":s,
                      "hits":hits(t,["goodsCd","C2104","C2103","dpstInfo","transaction",
                      "submission","service","action","target","금리","이율","interest",
                      "rate","ISA","퇴직연금","C0021"]),"text":t[:250000]}
                rr.append(item)
                print(" ",r.status_code,"score",s,r.url)
        except Exception as e:
            if "dpst" in u.lower(): rr.append({"url":u,"error":repr(e)})

    rr.sort(key=lambda x:x.get("score",0),reverse=True)
    result["resources"]=rr
    OUT_JSON.parent.mkdir(parents=True,exist_ok=True)
    OUT_JSON.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")

    lines=["="*120,"DB WebSquare Probe v1","="*120,
           "ISA goodsCd=C2104 / menuNum=1020",
           "IRP goodsCd=C2103 / menuNum=1021","",
           "="*120,"DPST INFO XML","="*120,
           result.get("detail_xml",{}).get("text",json.dumps(result.get("detail_xml",{}),ensure_ascii=False,indent=2)),
           "","="*120,"FOCUSED RESOURCE EVIDENCE","="*120]
    for i,item in enumerate(rr,1):
        lines += ["","-"*120,f"RESOURCE #{i}",f"URL={item.get('url')}",
                  f"HTTP={item.get('status')}",f"SCORE={item.get('score')}",""]
        if item.get("error"):
            lines.append("ERROR="+item["error"]);continue
        for h in item.get("hits",[])[:80]:
            lines += ["",f">>> HIT {h['keyword']} @ {h['position']}",h["context"]]
    OUT_TXT.write_text("\n".join(lines),encoding="utf-8")

    print("\n완료")
    print("JSON:",OUT_JSON)
    print("TXT :",OUT_TXT)
    print("보내줄 파일: data/db_websquare_probe_v1.txt")
    print("기존 ISA/IRP JSON은 수정하지 않습니다.")

if __name__=="__main__":
    main()
