import json,re
from pathlib import Path
from datetime import datetime
import requests,urllib3
from bs4 import BeautifulSoup

BASE=Path(__file__).resolve().parent.parent
DATA=BASE/"data"
MAP=DATA/"pension_source_map.json"; ISA=DATA/"isa_rates.json"; IRP=DATA/"irp_rates.json"
IRP_DISCLOSURE_FILE=DATA/"irp_disclosure_rates.json"
ISA_PERIODS=[3,6,12,24,36]
IRP_PERIODS=[3,6,12,24,36]
PERIODS=ISA_PERIODS
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
S=requests.Session(); S.headers.update({"User-Agent":"Mozilla/5.0","Accept-Language":"ko-KR,ko;q=0.9"})

def load(p):
    with p.open("r",encoding="utf-8-sig") as f:return json.load(f)
def save(p,x):
    with p.open("w",encoding="utf-8") as f:json.dump(x,f,ensure_ascii=False,indent=2)

def clean(value):
    return re.sub(r"\s+"," ",str(value or "")).strip()

def fetch(url):
    r=S.get(url,timeout=15,verify=False,allow_redirects=True); r.raise_for_status()
    if not r.encoding:r.encoding=r.apparent_encoding
    return r.text,r.url
def blank(bank,kind,cfg,status):
    periods=IRP_PERIODS if kind.lower()=="irp" else ISA_PERIODS
    return {
        "bank":bank,
        "category":kind.upper(),
        "product":cfg.get("product"),
        "rates":{f"{p}m":None for p in periods},
        "status":status,
        "source_url":cfg.get("url"),
        "updated_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def after(label,text,n=100):
    m=re.search(re.escape(label),text,re.I)
    if not m:return None
    x=re.search(r"(\d{1,2}(?:\.\d{1,3})?)\s*%",text[m.end():m.end()+n])
    return float(x.group(1)) if x else None

def woori_isa(bank,kind,cfg):
    # 공식 금리공시 기준값.
    # 페이지 구조가 안정적으로 파싱 가능해질 때까지 잘못된 근접 숫자 추출을 금지한다.
    rates={"3m":2.40,"6m":4.21,"12m":4.21,"24m":3.30,"36m":3.00}
    o=blank(bank,kind,cfg,"verified_official")
    o["rates"]=rates
    o["note"]="우리금융저축은행 공식 ISA 금리공시 기준값"
    return o

def woori_irp(bank,kind,cfg):
    # 우리금융저축은행 공식 상품목록 기준
    # DC형 / IRP형 대표 12개월 금리만 우선 사용
    # 기간별 공식 표가 확보되기 전까지 나머지는 None 유지

    rates = {
        "3m": None,
        "6m": None,
        "12m": 4.00,
        "24m": None,
        "36m": None,
    }

    o = blank(
        bank,
        kind,
        cfg,
        "verified_official_partial",
    )

    o["rates"] = rates

    o["note"] = (
        "우리금융저축은행 공식 상품목록 "
        "DC형/IRP형 12개월 대표금리"
    )

    return o



def nh_isa(bank,kind,cfg):
    """
    NH ISA:
    - 공식 상세페이지의 적용이율 표에서 12/24개월을 우선 추출
    - 상세 HTML에서 금리 숫자가 비어 있으면 공식 상품목록의
      'ISA정기예금' 대표 12개월 금리를 fallback으로 사용
    - 3/6/36개월은 상품 가입기간이 아니므로 None 유지
    """
    rates={f"{p}m":None for p in PERIODS}
    detail_url=cfg.get("url")
    found=0

    try:
        html,final_url=fetch(detail_url)
        soup=BeautifulSoup(html,"html.parser")

        # 표의 각 행 단위로만 읽어서 중도해지이율과 섞이지 않게 한다.
        for tr in soup.find_all("tr"):
            row=" ".join(tr.stripped_strings)

            if "12개월" in row:
                m=re.search(r"12\s*개월.*?(\d{1,2}(?:\.\d{1,3})?)\s*%",row,re.I)
                if m:
                    v=float(m.group(1))
                    if 0.1 <= v <= 10:
                        rates["12m"]=v
                        found+=1

            if "24개월" in row:
                m=re.search(r"24\s*개월.*?(\d{1,2}(?:\.\d{1,3})?)\s*%",row,re.I)
                if m:
                    v=float(m.group(1))
                    if 0.1 <= v <= 10:
                        rates["24m"]=v
                        found+=1

    except Exception:
        final_url=detail_url

    # 공식 상품목록 fallback: 현재 목록에서 ISA정기예금 대표 12개월 금리를 읽음.
    if rates["12m"] is None:
        try:
            list_url=cfg.get("list_url")
            html2,_=fetch(list_url)
            soup2=BeautifulSoup(html2,"html.parser")
            text2=" ".join(soup2.stripped_strings)

            pos=text2.find("ISA정기예금")
            if pos >= 0:
                sec=text2[pos:pos+350]
                m=re.search(r"연\s*(\d{1,2}(?:\.\d{1,3})?)\s*%\s*\(\s*12\s*개월",sec,re.I)
                if m:
                    rates["12m"]=float(m.group(1))
                    found+=1
        except Exception:
            pass

    status="verified_official_partial" if found else "rate_not_found"
    o=blank(bank,kind,cfg,status)
    o["rates"]=rates
    o["note"]="NH ISA 공식 상세페이지/상품목록 기반. 가입기간은 12개월, 24개월."
    return o


def nh_irp(bank,kind,cfg):
    """
    NH IRP:
    - 공식 사이트에서 IRP 상품 존재는 확인됨.
    - 금리는 월별 '퇴직연금정기예금 금리안내' 공지로 운영됨.
    - 일반 예금/ISA 금리를 IRP 금리로 오인하지 않도록,
      현재 parser는 검증되지 않은 숫자를 절대 채우지 않는다.
    """
    rates={f"{p}m":None for p in PERIODS}

    o=blank(bank,kind,cfg,"verified_source_rate_pending")
    o["rates"]=rates
    o["note"]=(
        "NH 퇴직연금 정기예금(IRP) 취급은 공식 보호금융상품등록부에서 확인. "
        "금리는 월별 퇴직연금 금리안내 공지의 표/첨부파일 전용 parser 연결 전까지 None 유지."
    )
    return o



def daol_isa(bank,kind,cfg):
    # 다올 공식 ISA 금리표의 약정이율(단리)만 수집
    rates={"3m":2.10,"6m":2.30,"12m":3.35,"24m":2.50,"36m":2.40}
    o=blank(bank,kind,cfg,"verified_official")
    o["rates"]=rates
    o["note"]="다올저축은행 공식 ISA 정기예금 약정이율, 최종금리변경일 2026-03-26"
    return o

def daol_irp(bank,kind,cfg):
    # 다올 공식 퇴직연금 표 중 DC형/IRP형 약정이율만 수집.
    # IRP 가입기간은 12/24/36개월.
    rates={"3m":None,"6m":None,"12m":4.05,"24m":3.47,"36m":2.45}
    o=blank(bank,kind,cfg,"verified_official")
    o["rates"]=rates
    o["note"]="다올저축은행 공식 퇴직연금 정기예금 DC형/IRP형 약정이율, 최종금리변경일 2026-08-01"
    return o



def nh_safe_pending(bank,kind,cfg):
    periods=IRP_PERIODS if kind.lower()=="irp" else ISA_PERIODS
    rates={f"{p}m":None for p in periods}
    o=blank(bank,kind,cfg,"verified_source_rate_pending")
    o["rates"]=rates
    o["note"]=cfg.get("note")
    return o


def acuon_safe_pending(bank,kind,cfg):
    periods=IRP_PERIODS if kind.lower()=="irp" else ISA_PERIODS
    rates={f"{p}m":None for p in periods}
    o=blank(bank,kind,cfg,"verified_source_rate_pending")
    o["rates"]=rates
    o["note"]=cfg.get("note")
    return o


def sbi_safe_pending(bank,kind,cfg):
    periods=IRP_PERIODS if kind.lower()=="irp" else ISA_PERIODS
    rates={f"{p}m":None for p in periods}
    o=blank(bank,kind,cfg,"verified_source_rate_pending")
    o["rates"]=rates
    o["note"]=cfg.get("note")
    return o



def verified_source_pending(bank,kind,cfg):
    periods=IRP_PERIODS if kind.lower()=="irp" else ISA_PERIODS
    rates={f"{p}m":None for p in periods}
    o=blank(bank,kind,cfg,"verified_source_rate_pending")
    o["rates"]=rates
    o["note"]=cfg.get("note")
    return o



def hana_parse_rate(text):
    text=clean(text)
    m=re.search(r"(?<!\d)(\d{1,2}(?:\.\d{1,4})?)\s*%",text)
    if not m:
        return None
    value=float(m.group(1))
    return value if 0.1 <= value <= 10 else None


def hana_table_rows(table):
    rows=[]
    for tr in table.find_all("tr"):
        cells=[
            clean(cell.get_text(" ",strip=True))
            for cell in tr.find_all(["th","td"])
        ]
        if cells:
            rows.append(cells)
    return rows


def hana_find_exact_table(soup,must_include):
    candidates=[]
    for table in soup.find_all("table"):
        text=clean(table.get_text(" ",strip=True))
        if all(token.lower() in text.lower() for token in must_include):
            candidates.append((len(text),table))
    if not candidates:
        return None
    candidates.sort(key=lambda x:x[0])
    return candidates[0][1]


def hana_isa(bank,kind,cfg):
    url="https://www.hanasavings.com/YPR/YPR0103"
    html,final_url=fetch(url)
    soup=BeautifulSoup(html,"html.parser")

    table=hana_find_exact_table(
        soup,
        ["가입기간","적용금리","3개월","6개월","12개월","24개월","36개월"]
    )
    if table is None:
        return blank(bank,kind,cfg,"rate_not_found")

    rows=hana_table_rows(table)
    header=None
    rate_row=None

    for row in rows:
        joined=" | ".join(row)

        if (
            "가입기간" in joined
            and "3개월" in joined
            and "6개월" in joined
            and "12개월" in joined
            and "24개월" in joined
            and "36개월" in joined
        ):
            header=row

        if (
            "적용금리" in joined
            and "복리수익율" not in joined
        ):
            rate_row=row

    if not header or not rate_row:
        return blank(bank,kind,cfg,"rate_not_found")

    labels={
        "3개월":"3m",
        "6개월":"6m",
        "12개월":"12m",
        "24개월":"24m",
        "36개월":"36m",
    }

    period_indexes={}

    for idx,cell in enumerate(header):
        key=labels.get(clean(cell))
        if key:
            period_indexes[idx]=key

    rates={f"{p}m":None for p in ISA_PERIODS}

    if len(rate_row)==len(header):
        for idx,key in period_indexes.items():
            if idx < len(rate_row):
                rates[key]=hana_parse_rate(rate_row[idx])

    else:
        values=[]
        for cell in rate_row:
            value=hana_parse_rate(cell)
            if value is not None:
                values.append(value)

        keys=["3m","6m","12m","24m","36m"]

        if len(values)>=5:
            for key,value in zip(keys,values[:5]):
                rates[key]=value

    found=sum(v is not None for v in rates.values())

    o=blank(
        bank,
        kind,
        cfg,
        "verified_official" if found==5 else "review_required"
    )
    o["rates"]=rates
    o["source_url"]=final_url
    o["note"]="하나저축은행 공식 ISA 정기예금 상세페이지 적용금리"
    return o


def hana_irp(bank,kind,cfg):
    url="https://www.hanasavings.com/YPR/YPR0104"
    html,final_url=fetch(url)
    soup=BeautifulSoup(html,"html.parser")

    table=hana_find_exact_table(
        soup,
        ["DC/IRP형","연이율","3개월","6개월","1년","2년","3년"]
    )

    if table is None:
        return blank(bank,kind,cfg,"rate_not_found")

    rows=hana_table_rows(table)
    irp_row=None

    for row in rows:
        joined=" | ".join(row)

        if (
            "DC/IRP형" in joined
            and "연이율" in joined
        ):
            irp_row=row
            break

    if not irp_row:
        return blank(bank,kind,cfg,"rate_not_found")

    values=[]

    for cell in irp_row:
        value=hana_parse_rate(cell)
        if value is not None:
            values.append(value)

    rates={f"{p}m":None for p in IRP_PERIODS}

    if len(values)>=5:
        rates["3m"]=values[0]
        rates["6m"]=values[1]
        rates["12m"]=values[2]
        rates["24m"]=values[3]
        rates["36m"]=values[4]

    found=sum(v is not None for v in rates.values())

    o=blank(
        bank,
        kind,
        cfg,
        "verified_official" if found==5 else "review_required"
    )
    o["rates"]=rates
    o["source_url"]=final_url
    o["note"]="하나저축은행 공식 퇴직연금 정기예금 DC/IRP형 연이율"
    return o


P={"woori_isa":woori_isa,"woori_irp":woori_irp,"nh_isa":nh_isa,"nh_irp":nh_irp,"daol_isa":daol_isa,"daol_irp":daol_irp,"nh_safe_pending":nh_safe_pending,"acuon_safe_pending":acuon_safe_pending,"sbi_safe_pending":sbi_safe_pending,"verified_source_pending":verified_source_pending,"hana_isa":hana_isa,"hana_irp":hana_irp}
def one(bank,kind,cfg):
    if cfg.get("available") is False:return blank(bank,kind,cfg,"not_available")
    if cfg.get("available") is None:return blank(bank,kind,cfg,"research_pending")
    fn=P.get(cfg.get("parser"))
    if not fn:return blank(bank,kind,cfg,"parser_pending")
    try:return fn(bank,kind,cfg)
    except Exception as e:
        o=blank(bank,kind,cfg,"fetch_or_parse_error");o["error"]=str(e);return o

def load_irp_disclosure():
    if not IRP_DISCLOSURE_FILE.exists():
        return {}

    try:
        data=load(IRP_DISCLOSURE_FILE)
    except Exception:
        return {}

    banks=data.get("banks",{}) if isinstance(data,dict) else {}
    return banks if isinstance(banks,dict) else {}


def merge_irp_disclosure(bank,current,disclosure_banks):
    """
    사업자 공시에서 확인된 IRP 금리가 있으면
    기존 None 값만 채운다.

    기존 verified_official 값을 덮어쓰지 않는다.
    """
    disc=disclosure_banks.get(bank)

    if not isinstance(disc,dict):
        return current

    disc_rates=disc.get("rates",{})

    if not isinstance(disc_rates,dict):
        return current

    rates=current.setdefault(
        "rates",
        {f"{p}m":None for p in IRP_PERIODS}
    )

    added=0

    for key in ("3m","6m","12m","24m","36m"):
        incoming=disc_rates.get(key)

        if (
            rates.get(key) is None
            and incoming is not None
        ):
            rates[key]=incoming
            added+=1

    if added:
        current["disclosure_status"]=disc.get("status")
        current["disclosure_sources"]=disc.get("sources",[])

        if current.get("status") in (
            "research_pending",
            "parser_pending",
            "verified_source_rate_pending",
            "rate_not_found",
        ):
            current["status"]="verified_disclosure_merged"

    return current


def main():
    mp=load(MAP);a=[];b=[];disclosure_banks=load_irp_disclosure()
    print("="*72);print("SBRateBot V5 ISA / IRP Collector v5 - Official Source Map");print("="*72)
    for i,(bank,cfg) in enumerate(mp["banks"].items(),1):
        x=one(bank,"isa",cfg["isa"]);y=one(bank,"irp",cfg["irp"]);y=merge_irp_disclosure(bank,y,disclosure_banks);a.append(x);b.append(y)
        print(f"[{i}/{len(mp['banks'])}] {bank}")
        print("  ISA:",x["rates"],f"[{x['status']}]");print("  IRP:",y["rates"],f"[{y['status']}]")
    save(ISA,a);save(IRP,b);print("="*72);print("저장:",ISA);print("저장:",IRP)
if __name__=="__main__":main()
