import requests
from datetime import datetime

BASE="https://www.idbsb.com"
PAGE_URL=BASE+"/w2/itb/dps/inr/dpstInrstGuidance.xml"
API_URL=BASE+"/itb/dps/inr/selectDpstInrstGuidance.do"

DS_PARAM={
"sn":"","inrstFdrmDpstDsmn":"10000000","inrstBilDsmn":"10000000",
"inrstFdrmSvingsMtPaymntAmt":"100000","inrstIsaFdrmDpstDsmn":"10000000",
"inrstGoodsInrstSeFdrmDpst":"1","inrstGoodsInrstSeBil":"1",
"inrstGoodsInrstSeFdrmSvings":"1","inrstGoodsInrstSeNrmltyDpst":"1",
"inrstGoodsInrstSeIsaFdrmDpst":"2","inrstGoodsGoodsSeFdrmDpst":"01",
"inrstGoodsGoodsSeBil":"11","inrstGoodsGoodsSeFdrmSvings":"21",
"inrstGoodsGoodsSeNrmltyDpst":"31","inrstGoodsGoodsSeIsaFdrmDpst":"01"
}
PERIOD_MAP={"3":"3m","6":"6m","12":"12m","24":"24m","36":"36m"}

def _date(v):
    v=str(v or "").strip()
    return f"{v[:4]}-{v[4:6]}-{v[6:8]}" if len(v)==8 and v.isdigit() else (v or None)

def collect_db_isa():
    s=requests.Session()
    s.headers.update({"User-Agent":"Mozilla/5.0","Accept":"application/json, text/plain, */*","Accept-Language":"ko-KR,ko;q=0.9"})
    s.get(PAGE_URL,timeout=30)
    r=s.post(API_URL,json={"ds_param":DS_PARAM},headers={
        "Origin":BASE,"Referer":PAGE_URL,"X-Requested-With":"XMLHttpRequest",
        "Content-Type":"application/json;charset=UTF-8"},timeout=30)
    r.raise_for_status()
    data=r.json()
    if data.get("errorCode"):
        raise RuntimeError(f"{data.get('errorCode')}: {data.get('errorMessage')}")
    rows=data.get("ds_inrstDtlIsaFdrmDpstList")
    if not isinstance(rows,list) or not rows:
        raise RuntimeError("DB official response has no ds_inrstDtlIsaFdrmDpstList")
    rates={k:None for k in ("3m","6m","12m","24m","36m")}
    for row in rows:
        key=PERIOD_MAP.get(str(row.get("pd","")).strip())
        val=row.get("intrtYy")
        if key and val not in (None,""):
            rates[key]=float(val)
    def find_date(obj):
        if isinstance(obj,dict):
            if obj.get("isaStdde"): return _date(obj["isaStdde"])
            for v in obj.values():
                x=find_date(v)
                if x:return x
        elif isinstance(obj,list):
            for v in obj:
                x=find_date(v)
                if x:return x
        return None
    return {"bank":"DB","product_type":"ISA","product_name":"ISA정기예금",
            "rates":rates,"effective_date":find_date(data),"source":"official",
            "status":"verified_official","source_url":PAGE_URL,"api_url":API_URL}

def collect_db():
    result={"bank":"DB","collected_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ISA":None,"IRP":None,"errors":{}}
    try: result["ISA"]=collect_db_isa()
    except Exception as e: result["errors"]["ISA"]=str(e)
    return result

def main():
    r=collect_db()
    print("="*72)
    print("SBRateBot V5 - DB Official ISA Collector")
    print("="*72)
    if r["ISA"]:
        x=r["ISA"]
        print("ISA:",x["product_name"])
        print("  rates:",x["rates"])
        print("  effective_date:",x["effective_date"])
        print("  status:",x["status"])
    else:
        print("ISA ERROR:",r["errors"].get("ISA"))
    print("IRP: 기존 pension_rates.py 공시 병합값 유지")
    if r["errors"]: raise SystemExit(1)

if __name__=="__main__":
    main()
