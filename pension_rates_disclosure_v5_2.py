import json,re
from pathlib import Path
from datetime import datetime
import requests,urllib3
from bs4 import BeautifulSoup

from ok import collect_ok
from db import collect_db

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


def acuon_api_post(product_code):
    """
    애큐온저축은행 공식 JEX 상품정보 API.
    POST /sd_TUB_GD_INFO_T.jct
    _JSON_={"GD_INFO_C":"상품코드"}
    """
    page_url = f"https://www.acuonsb.co.kr/sv_dpt{product_code}.act"
    api_url = "https://www.acuonsb.co.kr/sd_TUB_GD_INFO_T.jct"

    # 상품 페이지를 먼저 열어 브라우저 세션과 동일하게 준비
    try:
        S.get(
            page_url,
            timeout=20,
            verify=False,
            allow_redirects=True,
        )
    except Exception:
        pass

    payload_json = json.dumps(
        {"GD_INFO_C": str(product_code)},
        ensure_ascii=False,
        separators=(",", ":"),
    )

    r = S.post(
        api_url,
        data={"_JSON_": payload_json},
        timeout=30,
        verify=False,
        allow_redirects=True,
        headers={
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://www.acuonsb.co.kr",
            "Referer": page_url,
            "X-Requested-With": "XMLHttpRequest",
        },
    )
    r.raise_for_status()
    return r.json(), api_url


def acuon_rec001(payload):
    """
    애큐온 JEX 응답에서 REC_001 금리행을 재귀적으로 찾는다.
    """
    found = []

    def walk(obj):
        if isinstance(obj, dict):
            value = obj.get("REC_001")
            if isinstance(value, list):
                found.extend(x for x in value if isinstance(x, dict))
            elif isinstance(value, dict):
                found.append(value)

            for v in obj.values():
                walk(v)

        elif isinstance(obj, list):
            for v in obj:
                walk(v)

    walk(payload)
    return found


def acuon_month(value):
    text = clean(value)

    # API의 COND_TRM이 숫자 월 단위인 경우
    try:
        n = int(float(text))
        if n in (3, 6, 12, 24, 36):
            return n
    except Exception:
        pass

    m = re.search(r"(?<!\d)(3|6|12|24|36)\s*(?:개월|월)", text)
    if m:
        return int(m.group(1))

    m = re.search(r"(?<!\d)(1|2|3)\s*년", text)
    if m:
        return int(m.group(1)) * 12

    return None


def acuon_rate(value):
    text = clean(value).replace(",", "").replace("%", "")
    try:
        rate = float(text)
    except Exception:
        m = re.search(r"(-?\d{1,2}(?:\.\d{1,4})?)", text)
        if not m:
            return None
        rate = float(m.group(1))

    return rate if 0 <= rate <= 10 else None


def acuon_rates_from_rec001(rows, irp=False):
    """
    INT_TYPE=1 약정금리만 사용.
    IRP 응답에 DB/DC·IRP 행이 함께 있으면 DC/IRP 행만 우선한다.
    """
    rates = {f"{p}m": None for p in (IRP_PERIODS if irp else ISA_PERIODS)}

    selected = []

    for row in rows:
        if clean(row.get("INT_TYPE")) != "1":
            continue

        if irp:
            row_text = " ".join(clean(v) for v in row.values()).upper()
            # DB형과 DC/IRP형이 함께 있는 응답에서 DB형 제거
            if "DB" in row_text and "DC" not in row_text and "IRP" not in row_text:
                continue

        selected.append(row)

    # IRP 구분문구가 별도 필드에 없더라도 API의 DC/IRP 블록이
    # INT_TYPE=1로 반환되는 구조를 그대로 처리한다.
    for row in selected:
        month = acuon_month(row.get("COND_TRM"))
        if month not in (3, 6, 12, 24, 36):
            continue

        rate = acuon_rate(row.get("CONT_APLY_INT"))
        if rate is None:
            continue

        key = f"{month}m"

        # 동일 기간이 여러 번 나오면 IRP/DC 문구가 있는 행을 우선
        if rates[key] is None:
            rates[key] = rate
        elif irp:
            row_text = " ".join(clean(v) for v in row.values()).upper()
            if "DC" in row_text or "IRP" in row_text:
                rates[key] = rate

    return rates


def acuon_isa(bank,kind,cfg):
    """
    애큐온저축은행 ISA 정기예금.
    GD_INFO_C=1201170 / REC_001 / INT_TYPE=1 /
    COND_TRM별 CONT_APLY_INT 약정금리.
    """
    try:
        payload, api_url = acuon_api_post("1201170")
        rows = acuon_rec001(payload)
        rates = acuon_rates_from_rec001(rows, irp=False)
        found = sum(v is not None for v in rates.values())

        status = (
            "verified_official"
            if found == 5
            else "verified_official_partial"
            if found
            else "rate_not_found"
        )

        o = blank(bank,kind,cfg,status)
        o["rates"] = rates
        o["source_url"] = api_url
        o["note"] = (
            "애큐온저축은행 공식 JEX 상품정보 API. "
            "GD_INFO_C=1201170, REC_001의 INT_TYPE=1 약정금리 중 "
            "COND_TRM별 CONT_APLY_INT 사용."
        )
        return o

    except Exception as error:
        o = blank(bank,kind,cfg,"fetch_or_parse_error")
        o["note"] = f"애큐온 ISA 공식 API 수집 실패: {error}"
        o["error"] = str(error)
        return o


def acuon_irp(bank,kind,cfg):
    """
    애큐온저축은행 퇴직연금 정기예금 DC/IRP형.
    GD_INFO_C=1201171 / REC_001 / INT_TYPE=1 /
    COND_TRM별 CONT_APLY_INT 약정금리.
    """
    try:
        payload, api_url = acuon_api_post("1201171")
        rows = acuon_rec001(payload)
        rates = acuon_rates_from_rec001(rows, irp=True)
        found = sum(v is not None for v in rates.values())

        status = (
            "verified_official"
            if found == 5
            else "verified_official_partial"
            if found
            else "rate_not_found"
        )

        o = blank(bank,kind,cfg,status)
        o["rates"] = rates
        o["source_url"] = api_url
        o["note"] = (
            "애큐온저축은행 공식 JEX 퇴직연금 상품정보 API. "
            "GD_INFO_C=1201171의 DC/IRP형 약정금리만 사용. "
            "REC_001, INT_TYPE=1, COND_TRM별 CONT_APLY_INT 기준."
        )
        return o

    except Exception as error:
        o = blank(bank,kind,cfg,"fetch_or_parse_error")
        o["note"] = f"애큐온 IRP 공식 API 수집 실패: {error}"
        o["error"] = str(error)
        return o


def acuon_safe_pending(bank,kind,cfg):
    # 이전 source map과의 호환용. 새 source map에서는 acuon_isa/acuon_irp 사용.
    return acuon_irp(bank,kind,cfg) if kind.lower()=="irp" else acuon_isa(bank,kind,cfg)


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



def shinhan_api_post(page_path, api_path, pd_cd):
    """
    신한저축은행 SPA 공식 상품 API 호출.
    - 상품 페이지 GET으로 세션을 먼저 연다.
    - /api/... endpoint에 JSON POST.
    """
    page_url = "https://www.shinhansavings.com" + page_path
    api_url = "https://www.shinhansavings.com/api" + api_path

    # 세션/쿠키 준비
    S.get(
        page_url,
        timeout=20,
        verify=False,
        allow_redirects=True,
    )

    r = S.post(
        api_url,
        json={"PD_CD": pd_cd},
        timeout=30,
        verify=False,
        headers={
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://www.shinhansavings.com",
            "Referer": page_url,
            "X-Requested-With": "XMLHttpRequest",
        },
    )
    r.raise_for_status()

    return r.json(), api_url


def shinhan_rows(payload, key):
    """
    payload.data.<key>.LIST 추출.
    row가 {'map': {...}} 형태면 map을 벗긴다.
    """
    data = payload.get("data", payload)

    block = data.get(key, {}) if isinstance(data, dict) else {}
    rows = block.get("LIST", []) if isinstance(block, dict) else []

    result = []

    if isinstance(rows, list):
        for row in rows:
            if isinstance(row, dict) and isinstance(row.get("map"), dict):
                result.append(row["map"])
            elif isinstance(row, dict):
                result.append(row)

    return result


def shinhan_rates_by_fm_term(rows, allowed_class=None, allowed_name=None):
    """
    dscr10220.LIST의 FM_TERM을 실제 계약기간 기준으로 사용.
    APLY_RATE = 약정 연이율.

    예:
      FM_TERM=3  -> 3개월 금리
      FM_TERM=6  -> 6개월 금리
      FM_TERM=12 -> 12개월 금리
      FM_TERM=24 -> 24개월 금리
      FM_TERM=36 -> 36개월 금리
    """
    rates = {
        "3m": None,
        "6m": None,
        "12m": None,
        "24m": None,
        "36m": None,
    }

    for row in rows:
        class_cd = str(row.get("CLASS_CD", "")).strip()
        class_nm = str(row.get("CLASS_NM", "")).strip()

        if allowed_class is not None and class_cd != str(allowed_class):
            continue

        if allowed_name is not None and allowed_name not in class_nm:
            continue

        try:
            month = int(float(str(row.get("FM_TERM")).strip()))
        except Exception:
            continue

        if month not in (3, 6, 12, 24, 36):
            continue

        try:
            rate = float(str(row.get("APLY_RATE")).strip())
        except Exception:
            continue

        if not (0 <= rate <= 10):
            continue

        rates[f"{month}m"] = rate

    return rates


def shinhan_isa(bank, kind, cfg):
    """
    신한저축은행 ISA정기예금
    공식 API:
      POST /api/PD0080/selectSavPd.json
      PD_CD = 24014

    dscr10220.LIST:
      CLASS_CD 24014 = ISA정기예금
      FM_TERM = 계약기간 시작월
      APLY_RATE = 약정 연이율

    현재 공식 가입기간: 3/6/12/24개월.
    36개월은 미제공이므로 None.
    """
    try:
        payload, api_url = shinhan_api_post(
            "/PD_0080",
            "/PD0080/selectSavPd.json",
            24014,
        )

        rows = shinhan_rows(payload, "dscr10220")

        rates = shinhan_rates_by_fm_term(
            rows,
            allowed_class="24014",
        )

        # 현재 상품 가입기간은 최대 24개월.
        rates["36m"] = None

        found = sum(v is not None for v in rates.values())

        status = (
            "verified_official"
            if found >= 4
            else "verified_official_partial"
            if found
            else "rate_not_found"
        )

        o = blank(bank, kind, cfg, status)
        o["rates"] = rates
        o["source_url"] = api_url
        o["note"] = (
            "신한저축은행 공식 ISA정기예금 API. "
            "dscr10220.LIST의 CLASS_CD=24014, "
            "FM_TERM별 APLY_RATE 약정이율 사용. "
            "공식 가입기간 3/6/12/24개월, 36개월 미제공."
        )
        return o

    except Exception as error:
        o = blank(bank, kind, cfg, "fetch_or_parse_error")
        o["note"] = f"신한 ISA 공식 API 수집 실패: {error}"
        return o


def shinhan_irp(bank, kind, cfg):
    """
    신한저축은행 퇴직연금 정기예금 - DC/IRP형

    공식 API:
      POST /api/PD0081/selectSavPd.json
      PD_CD = 24015

    주의:
    - dscr10230.LIST의 12개월 대표금리(예: 4.05%)는 DB형 표시값.
    - IRP 모니터링은 dscr10220.LIST에서
      CLASS_CD=24016 / CLASS_NM='퇴직연금정기예금(DC/IRP)'
      의 APLY_RATE를 사용한다.
    """
    try:
        payload, api_url = shinhan_api_post(
            "/PD_0081",
            "/PD0081/selectSavPd.json",
            24015,
        )

        rows = shinhan_rows(payload, "dscr10220")

        rates = shinhan_rates_by_fm_term(
            rows,
            allowed_class="24016",
        )

        found = sum(v is not None for v in rates.values())

        status = (
            "verified_official"
            if found == 5
            else "verified_official_partial"
            if found
            else "rate_not_found"
        )

        o = blank(bank, kind, cfg, status)
        o["rates"] = rates
        o["source_url"] = api_url
        o["note"] = (
            "신한저축은행 공식 퇴직연금 정기예금 API. "
            "DC/IRP형(CLASS_CD=24016)의 FM_TERM별 "
            "APLY_RATE 약정이율 사용. "
            "DB형 대표금리(dscr10230)는 IRP 금리로 사용하지 않음."
        )
        return o

    except Exception as error:
        o = blank(bank, kind, cfg, "fetch_or_parse_error")
        o["note"] = f"신한 IRP 공식 API 수집 실패: {error}"
        return o



def kb_item_info(item_code):
    """
    KB저축은행 공식 WebSquare 상품정보 JSON 서비스.

    v5.14:
    WebSquare가 화면별로 JSON wrapper 형태를 다르게 받는 경우가 있어
    v6 단독 테스트에서 사용한 payload 후보를 순차 시도한다.
    """
    page_url = (
        "https://www.kbsavings.com/websquare/websquare.jsp"
        "?w2xPath=/jsp/depositItemInfo/depositItemInfo.xml"
        f"&ITEM_CODE={item_code}"
    )
    api_url = (
        "https://www.kbsavings.com/websquare/engine/callJsonService.jsp"
        "?serviceID=S_CommonItemService_getItemInfo"
    )

    # 브라우저와 유사하게 상품 상세 화면을 먼저 열어 세션 준비
    warm = S.get(
        page_url,
        timeout=30,
        verify=False,
        allow_redirects=True,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/142.0 Safari/537.36"
            ),
            "Accept": (
                "text/html,application/xhtml+xml,"
                "application/xml;q=0.9,*/*;q=0.8"
            ),
        },
    )
    warm.raise_for_status()

    payloads = [
        {"ITEM_CODE": item_code},
        {"SEARCH": {"ITEM_CODE": item_code}},
        {"data": {"ITEM_CODE": item_code}},
        {"DATA": {"ITEM_CODE": item_code}},
    ]

    errors = []

    for payload_no, request_payload in enumerate(payloads, start=1):
        try:
            r = S.post(
                api_url,
                json=request_payload,
                timeout=30,
                verify=False,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/142.0 Safari/537.36"
                    ),
                    "Accept": "application/json, text/plain, */*",
                    "Content-Type": "application/json;charset=UTF-8",
                    "Origin": "https://www.kbsavings.com",
                    "Referer": page_url,
                    "X-Requested-With": "XMLHttpRequest",
                },
            )
            r.raise_for_status()

            payload = r.json()
            data = payload.get("DATA", payload)

            if not isinstance(data, dict):
                errors.append(
                    f"payload#{payload_no}: DATA block not found"
                )
                continue

            result = data.get("RESULT") or {}
            info = data.get("RESULT_ITEM_INFO") or []
            summary = data.get("RESULT_ITEM_SUMMARY") or []

            if isinstance(result, list):
                result = result[0] if result else {}

            if not isinstance(result, dict):
                result = {}

            if not isinstance(info, list):
                info = []

            if not isinstance(summary, list):
                summary = []

            item_name = clean(
                result.get("ITEM_NAME")
            )

            if item_name:
                return (
                    result,
                    info,
                    summary,
                    api_url,
                    payload_no,
                )

            errors.append(
                f"payload#{payload_no}: ITEM_NAME empty"
            )

        except Exception as error:
            errors.append(
                f"payload#{payload_no}: {error}"
            )

    raise ValueError(
        "KB official API request failed | "
        + " | ".join(errors)
    )


def kb_info_html(info_rows, name):
    """
    RESULT_ITEM_INFO에서 특정 GUBN_NAME의 CONTENT_HTML/CONTENT 반환.
    """
    for row in info_rows:
        if not isinstance(row, dict):
            continue

        if clean(row.get("GUBN_NAME")) == name:
            return (
                row.get("CONTENT_HTML")
                or row.get("CONTENT")
                or ""
            )

    return ""


def kb_table_rows(content_html):
    """
    HTML 표를 행/열 텍스트 배열로 변환.
    """
    soup = BeautifulSoup(
        str(content_html or ""),
        "html.parser",
    )

    rows = []

    for tr in soup.find_all("tr"):
        cells = [
            clean(cell.get_text(" ", strip=True))
            for cell in tr.find_all(["th", "td"])
        ]

        if cells:
            rows.append(cells)

    return rows


def kb_month(value):
    text = clean(value)

    m = re.search(
        r"(?<!\d)(3|6|12|24|36)\s*개월",
        text,
    )
    if m:
        return int(m.group(1))

    # 퇴직연금 표는 1년/2년/3년 형태
    m = re.search(
        r"(?<!\d)(1|2|3)\s*년",
        text,
    )
    if m:
        return int(m.group(1)) * 12

    return None


def kb_rate(value):
    text = clean(value).replace(",", "")

    m = re.search(
        r"(-?\d{1,2}(?:\.\d{1,3})?)\s*%",
        text,
    )

    if not m:
        # 셀에 % 기호가 빠진 경우 보완
        m = re.fullmatch(
            r"\s*(-?\d{1,2}(?:\.\d{1,3})?)\s*",
            text,
        )

    if not m:
        return None

    value = float(m.group(1))

    if not (0 <= value <= 10):
        return None

    return value


def kb_parse_isa_rate_table(content_html):
    """
    ISA정기예금 이율안내의 '적용이율'만 추출.
    복리수익률 / 중도해지이율은 제외한다.

    지원 구조:
    1) 열형: 기간 | 3개월 | 6개월 | ...
             적용이율 | 2.0% | 2.2% | ...
    2) 행형: 3개월 | 2.0%
    """
    rates = {
        "3m": None,
        "6m": None,
        "12m": None,
        "24m": None,
        "36m": None,
    }

    rows = kb_table_rows(content_html)

    # 1) 열형 표
    period_row = None
    rate_row = None

    for row in rows:
        joined = " ".join(row)

        if (
            "기간" in joined
            and sum(
                kb_month(cell) is not None
                for cell in row
            ) >= 3
        ):
            period_row = row

        if (
            row
            and (
                "적용이율" in row[0]
                or row[0] == "이율"
            )
            and len(row) >= 4
        ):
            rate_row = row

        if period_row and rate_row:
            break

    if period_row and rate_row:
        months = [
            kb_month(cell)
            for cell in period_row
            if kb_month(cell) is not None
        ]
        values = [
            kb_rate(cell)
            for cell in rate_row[1:]
        ]

        values = [
            value
            for value in values
            if value is not None
        ]

        if len(months) == len(values):
            for month, value in zip(months, values):
                if month in ISA_PERIODS:
                    rates[f"{month}m"] = value

    # 2) 행형 보완
    for row in rows:
        if len(row) < 2:
            continue

        month = kb_month(row[0])
        if month not in ISA_PERIODS:
            continue

        # 해당 행에서 첫 금리값만 사용
        value = None

        for cell in row[1:]:
            value = kb_rate(cell)
            if value is not None:
                break

        if (
            value is not None
            and rates[f"{month}m"] is None
        ):
            rates[f"{month}m"] = value

    return rates


def kb_parse_irp_rate_table(content_html):
    """
    퇴직연금 정기예금 표에서 DC/IRP '약정이율' 열만 추출.
    DB형 / 연수익률 / 중도해지이율은 제외한다.
    """
    rates = {
        "3m": None,
        "6m": None,
        "12m": None,
        "24m": None,
        "36m": None,
    }

    rows = kb_table_rows(content_html)

    header_index = None
    dc_irp_index = None

    # 가장 최근 표를 우선하기 위해 뒤에서부터 탐색
    for idx in range(len(rows) - 1, -1, -1):
        row = rows[idx]

        for col_idx, cell in enumerate(row):
            normalized = (
                cell.replace(" ", "")
                .replace("\xa0", "")
                .upper()
            )

            if (
                "DC/IRP" in normalized
                and "약정이율" in normalized
            ):
                header_index = idx
                dc_irp_index = col_idx
                break

        if dc_irp_index is not None:
            break

    if dc_irp_index is not None:
        for row in rows[header_index + 1:]:
            if not row:
                continue

            month = kb_month(row[0])

            if month not in IRP_PERIODS:
                # 다음 섹션에 들어가면 종료
                joined = " ".join(row)
                if (
                    rates["3m"] is not None
                    and (
                        "중도해지" in joined
                        or "만기후" in joined
                    )
                ):
                    break
                continue

            if dc_irp_index >= len(row):
                continue

            value = kb_rate(
                row[dc_irp_index]
            )

            if value is not None:
                rates[f"{month}m"] = value

    # HTML이 비정상적으로 펼쳐진 경우 텍스트 기반 최종 보완.
    # 현재 KB 표의 순서는:
    # 계약기간 / DB약정 / DB수익률 / DC/IRP약정 / DC/IRP수익률
    if sum(v is not None for v in rates.values()) < 5:
        text = clean(
            BeautifulSoup(
                str(content_html or ""),
                "html.parser",
            ).get_text(" ", strip=True)
        )

        # 최신 기준일 블록이 있으면 마지막 블록 사용
        sections = re.split(
            r"(?=기준일\s*\d{4}\.\d{1,2}\.\d{1,2})",
            text,
        )
        current = sections[-1] if sections else text

        pattern = re.compile(
            r"(3개월|6개월|1년|2년|3년)"
            r"\s+"
            r"(\d+(?:\.\d+)?)\s*%"
            r"\s+"
            r"(\d+(?:\.\d+)?)\s*%"
            r"\s+"
            r"(\d+(?:\.\d+)?)\s*%"
            r"\s+"
            r"(\d+(?:\.\d+)?)\s*%",
            re.I,
        )

        for m in pattern.finditer(current):
            month = kb_month(m.group(1))
            value = float(m.group(4))  # DC/IRP 약정이율

            if (
                month in IRP_PERIODS
                and 0 <= value <= 10
            ):
                rates[f"{month}m"] = value

    return rates


def kb_isa(bank, kind, cfg):
    """
    KB저축은행 ISA정기예금
    ITEM_CODE=IB13
    공식 상품정보 API의 이율안내 > 적용이율 사용.
    """
    try:
        result, info, summary, api_url, payload_no = kb_item_info("IB13")

        product_name = clean(
            result.get("ITEM_NAME")
        )

        if "ISA정기예금" not in product_name:
            raise ValueError(
                f"Unexpected KB ISA product: {product_name}"
            )

        content_html = kb_info_html(
            info,
            "이율안내",
        )

        rates = kb_parse_isa_rate_table(
            content_html
        )

        found = sum(
            v is not None
            for v in rates.values()
        )

        status = (
            "verified_official"
            if found == 5
            else "verified_official_partial"
            if found
            else "rate_not_found"
        )

        o = blank(bank, kind, cfg, status)
        o["rates"] = rates
        o["source_url"] = api_url
        o["note"] = (
            "KB저축은행 공식 WebSquare 상품정보 API. "
            "ITEM_CODE=IB13(ISA정기예금)의 이율안내 표에서 "
            "기간별 적용이율만 수집. "
            "복리수익률/중도해지이율 제외. "
            f"API payload#{payload_no} 사용."
        )
        return o

    except Exception as error:
        o = blank(
            bank,
            kind,
            cfg,
            "fetch_or_parse_error",
        )
        o["note"] = (
            f"KB ISA 공식 API 수집 실패: {error}"
        )
        o["error"] = str(error)
        return o


def kb_irp(bank, kind, cfg):
    """
    KB저축은행 퇴직연금 정기예금
    ITEM_CODE=IB18
    공식 상품정보 API의 이율안내에서
    DC/IRP(약정이율) 열만 수집.
    """
    try:
        result, info, summary, api_url, payload_no = kb_item_info("IB18")

        product_name = clean(
            result.get("ITEM_NAME")
        )

        if "퇴직연금" not in product_name:
            raise ValueError(
                f"Unexpected KB IRP product: {product_name}"
            )

        content_html = kb_info_html(
            info,
            "이율안내",
        )

        rates = kb_parse_irp_rate_table(
            content_html
        )

        found = sum(
            v is not None
            for v in rates.values()
        )

        status = (
            "verified_official"
            if found == 5
            else "verified_official_partial"
            if found
            else "rate_not_found"
        )

        o = blank(bank, kind, cfg, status)
        o["rates"] = rates
        o["source_url"] = api_url
        o["note"] = (
            "KB저축은행 공식 WebSquare 상품정보 API. "
            "ITEM_CODE=IB18(퇴직연금 정기예금)의 "
            "DC/IRP(약정이율)만 수집. "
            "DB형/연수익률/중도해지이율 제외. "
            f"API payload#{payload_no} 사용."
        )
        return o

    except Exception as error:
        o = blank(
            bank,
            kind,
            cfg,
            "fetch_or_parse_error",
        )
        o["note"] = (
            f"KB IRP 공식 API 수집 실패: {error}"
        )
        o["error"] = str(error)
        return o



# ============================================================
# OK저축은행 공식 ISA / IRP Collector Adapter
# ============================================================

_OK_CACHE=None

def get_ok_official():
    global _OK_CACHE
    if _OK_CACHE is None:
        _OK_CACHE=collect_ok()
    return _OK_CACHE

def ok_official(bank,kind,cfg):
    result=get_ok_official()
    product_type=kind.upper()
    item=result.get(product_type)

    if not isinstance(item,dict):
        o=blank(bank,kind,cfg,"fetch_or_parse_error")
        error=result.get("errors",{}).get(
            product_type,
            "OK official collector returned no data"
        )
        o["error"]=str(error)
        o["note"]=f"OK저축은행 공식 {product_type} API 수집 실패: {error}"
        return o

    periods=IRP_PERIODS if kind.lower()=="irp" else ISA_PERIODS
    o=blank(bank,kind,cfg,item.get("status","verified_official"))
    o["product"]=item.get("product_name") or cfg.get("product")
    o["rates"]=item.get("rates",{f"{p}m":None for p in periods})
    o["source_url"]=item.get("source_url") or cfg.get("url")
    o["effective_date"]=item.get("effective_date")
    o["depsGdsSqno"]=item.get("depsGdsSqno")
    o["note"]=(
        "OK저축은행 공식 홈페이지 상품정보 API 자동수집. "
        f"{product_type} / depsGdsSqno={item.get('depsGdsSqno')} / "
        f"시행일={item.get('effective_date') or '-'}"
    )
    return o

def ok_isa(bank,kind,cfg):
    return ok_official(bank,kind,cfg)

def ok_irp(bank,kind,cfg):
    return ok_official(bank,kind,cfg)


# ============================================================
# 한국투자저축은행 공식 ISA / IRP Collector Adapter
# - 기존 성공 통합본 로직은 건드리지 않음
# - 한국투자만 Selenium + WebSquare 렌더링 DOM으로 수집
# ============================================================

_KOREAINVEST_CACHE=None

KOREAINVEST_TARGETS={
    "ISA":{
        "url":"https://sb.koreainvestment.com/?PRD-PDS001-10#",
        "expected_title":"ISA정기예금",
    },
    "IRP":{
        "url":"https://sb.koreainvestment.com/?PRD-PDS001-11#",
        "expected_title":"퇴직연금정기예금",
    },
}


def koreainvest_clean(value):
    return re.sub(
        r"\s+",
        " ",
        str(value or "").replace("\xa0"," ")
    ).strip()


def koreainvest_rate(value):
    m=re.search(
        r"(\d+(?:\.\d+)?)",
        koreainvest_clean(value)
    )

    if not m:
        return None

    try:
        v=float(m.group(1))
    except Exception:
        return None

    return v if 0 <= v <= 10 else None


def koreainvest_period(value):
    m=re.search(
        r"(\d+)\s*개월",
        koreainvest_clean(value)
    )

    if not m:
        return None

    try:
        return int(m.group(1))
    except Exception:
        return None


def koreainvest_reference_date(value):
    m=re.search(
        r"(\d{4})\s*년\s*(\d{1,2})\s*월\s*(\d{1,2})\s*일",
        koreainvest_clean(value)
    )

    if not m:
        return None

    y,mn,d=map(int,m.groups())

    return f"{y:04d}-{mn:02d}-{d:02d}"


def koreainvest_month_key(value):
    m=re.search(
        r"(\d{4})\D+(\d{1,2})",
        koreainvest_clean(value)
    )

    if not m:
        return (0,0)

    return (
        int(m.group(1)),
        int(m.group(2)),
    )


def koreainvest_create_driver():
    """
    회사 PC에서 검증된 Microsoft Edge 우선.
    실패 시 Chrome으로 자동 전환.
    """
    edge_error=None

    try:
        from selenium import webdriver
        from selenium.webdriver.edge.options import Options as EdgeOptions

        options=EdgeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1600,1200")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")

        driver=webdriver.Edge(options=options)
        driver.set_page_load_timeout(30)

        return driver,"Edge"

    except Exception as e:
        edge_error=e

    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options as ChromeOptions

        options=ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1600,1200")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")

        driver=webdriver.Chrome(options=options)
        driver.set_page_load_timeout(30)

        return driver,"Chrome"

    except Exception as chrome_error:
        raise RuntimeError(
            "한국투자 Edge/Chrome WebDriver 실행 실패 | "
            f"Edge={edge_error} | Chrome={chrome_error}"
        )


def koreainvest_wait(driver,expected_title):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    wait=WebDriverWait(driver,30)

    wait.until(
        EC.presence_of_element_located(
            (
                By.ID,
                "mf_wfm_contents_intrGridView"
            )
        )
    )

    wait.until(
        lambda d:
            expected_title in koreainvest_clean(d.title)
            or expected_title in koreainvest_clean(
                d.find_element(By.TAG_NAME,"body").text
            )
    )


def koreainvest_section(driver):
    return driver.execute_script(
        r"""
        const root=document.getElementById(
            "mf_wfm_contents_intrGridView"
        );

        if(!root){
            return null;
        }

        return {
            text:(root.innerText || "")
                .replace(/\s+/g," ")
                .trim(),

            tables:Array.from(
                root.querySelectorAll("table")
            ).map(
                (table,tableIndex)=>({
                    tableIndex,
                    rows:Array.from(
                        table.querySelectorAll("tr")
                    ).map(
                        row=>Array.from(
                            row.querySelectorAll("th, td")
                        ).map(
                            cell=>({
                                text:(cell.innerText || "")
                                    .replace(/\s+/g," ")
                                    .trim(),
                                tag:cell.tagName,
                                rowspan:cell.getAttribute("rowspan") || "1",
                                colspan:cell.getAttribute("colspan") || "1"
                            })
                        )
                    )
                })
            )
        };
        """
    )


def koreainvest_parse_isa(bank,cfg,section):
    rates={f"{p}m":None for p in ISA_PERIODS}

    if not section:
        o=blank(bank,"isa",cfg,"rate_not_found")
        o["note"]="한국투자 ISA WebSquare 금리영역 미확인"
        return o

    for table in section.get("tables",[]):
        found=0

        for row in table.get("rows",[]):
            texts=[
                koreainvest_clean(cell.get("text"))
                for cell in row
            ]

            if len(texts) < 2:
                continue

            period=koreainvest_period(texts[0])

            if period not in ISA_PERIODS:
                continue

            rate=koreainvest_rate(texts[1])

            if rate is None:
                continue

            rates[f"{period}m"]=rate
            found+=1

        if found >= 3:
            break

    found=sum(v is not None for v in rates.values())

    status=(
        "verified_official"
        if found==5
        else "verified_official_partial"
        if found
        else "rate_not_found"
    )

    o=blank(bank,"isa",cfg,status)
    o["product"]="ISA정기예금"
    o["rates"]=rates
    o["source_url"]=KOREAINVEST_TARGETS["ISA"]["url"]
    o["reference_date"]=koreainvest_reference_date(
        section.get("text","")
    )
    o["collector"]="koreainvest_websquare_selenium"
    o["note"]=(
        "한국투자저축은행 공식 WebSquare ISA정기예금 금리안내 표 자동수집."
    )

    return o


def koreainvest_parse_irp(bank,cfg,section):
    rates={f"{p}m":None for p in IRP_PERIODS}
    db_rates={f"{p}m":None for p in IRP_PERIODS}
    rate_months={}

    if not section:
        o=blank(bank,"irp",cfg,"rate_not_found")
        o["note"]="한국투자 IRP WebSquare 금리영역 미확인"
        return o

    target_rows=[]

    for table in section.get("tables",[]):
        rows=table.get("rows",[])

        joined=" ".join(
            koreainvest_clean(cell.get("text"))
            for row in rows
            for cell in row
        )

        if "DC/IRP형" in joined and "DB형" in joined:
            target_rows=rows
            break

    if not target_rows:
        o=blank(bank,"irp",cfg,"rate_not_found")
        o["note"]="한국투자 IRP DC/IRP형/DB형 금리표 미확인"
        return o

    period_rows={}
    current_period=None

    for row in target_rows:
        cells=[
            cell
            for cell in row
            if cell.get("tag")=="TD"
        ]

        texts=[
            koreainvest_clean(cell.get("text"))
            for cell in cells
        ]

        if not texts:
            continue

        first_period=koreainvest_period(texts[0])

        if first_period in IRP_PERIODS:
            current_period=first_period

            if len(texts) < 4:
                continue

            rate_month=texts[1]
            dc_irp=koreainvest_rate(texts[2])
            db=koreainvest_rate(texts[3])

        else:
            if current_period is None or len(texts) < 3:
                continue

            rate_month=texts[0]
            dc_irp=koreainvest_rate(texts[1])
            db=koreainvest_rate(texts[2])

        if dc_irp is None and db is None:
            continue

        period_rows.setdefault(
            current_period,
            []
        ).append({
            "rate_month":rate_month,
            "dc_irp_rate":dc_irp,
            "db_rate":db,
        })

    for period in IRP_PERIODS:
        rows=period_rows.get(period,[])

        if not rows:
            continue

        latest=max(
            rows,
            key=lambda x:koreainvest_month_key(
                x.get("rate_month")
            )
        )

        rates[f"{period}m"]=latest.get("dc_irp_rate")
        db_rates[f"{period}m"]=latest.get("db_rate")
        rate_months[f"{period}m"]=latest.get("rate_month")

    found=sum(v is not None for v in rates.values())

    status=(
        "verified_official"
        if found==5
        else "verified_official_partial"
        if found
        else "rate_not_found"
    )

    o=blank(bank,"irp",cfg,status)
    o["product"]="퇴직연금정기예금"
    o["rates"]=rates
    o["db_rates"]=db_rates
    o["rate_months"]=rate_months
    o["source_url"]=KOREAINVEST_TARGETS["IRP"]["url"]
    o["reference_date"]=koreainvest_reference_date(
        section.get("text","")
    )
    o["collector"]="koreainvest_websquare_selenium"
    o["note"]=(
        "한국투자저축은행 공식 WebSquare 퇴직연금정기예금 금리표 자동수집. "
        "통합 IRP 대표금리는 DC/IRP형을 사용하고 DB형은 db_rates에 별도 보존."
    )

    return o


def collect_koreainvest_official(bank,cfg):
    driver=None

    try:
        driver,browser=koreainvest_create_driver()

        results={}

        for kind,target in KOREAINVEST_TARGETS.items():
            driver.get(target["url"])
            koreainvest_wait(
                driver,
                target["expected_title"]
            )
            section=koreainvest_section(driver)

            if kind=="ISA":
                results["ISA"]=koreainvest_parse_isa(
                    bank,
                    cfg["isa"],
                    section
                )
            else:
                results["IRP"]=koreainvest_parse_irp(
                    bank,
                    cfg["irp"],
                    section
                )

        results["browser"]=browser
        return results

    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass


def get_koreainvest_official(bank,cfg):
    global _KOREAINVEST_CACHE

    if _KOREAINVEST_CACHE is None:
        _KOREAINVEST_CACHE=collect_koreainvest_official(
            bank,
            cfg
        )

    return _KOREAINVEST_CACHE


def koreainvest_isa(bank,kind,cfg,bank_cfg=None):
    result=get_koreainvest_official(
        bank,
        bank_cfg
    )

    item=result.get("ISA")

    if isinstance(item,dict):
        return item

    return blank(
        bank,
        kind,
        cfg,
        "fetch_or_parse_error"
    )


def koreainvest_irp(bank,kind,cfg,bank_cfg=None):
    result=get_koreainvest_official(
        bank,
        bank_cfg
    )

    item=result.get("IRP")

    if isinstance(item,dict):
        return item

    return blank(
        bank,
        kind,
        cfg,
        "fetch_or_parse_error"
    )


P={"woori_isa":woori_isa,"woori_irp":woori_irp,"nh_isa":nh_isa,"nh_irp":nh_irp,"daol_isa":daol_isa,"daol_irp":daol_irp,"nh_safe_pending":nh_safe_pending,"acuon_safe_pending":acuon_safe_pending,"acuon_isa":acuon_isa,"acuon_irp":acuon_irp,"sbi_safe_pending":sbi_safe_pending,"verified_source_pending":verified_source_pending,"hana_isa":hana_isa,"hana_irp":hana_irp,"shinhan_isa":shinhan_isa,"shinhan_irp":shinhan_irp,"kb_isa":kb_isa,"kb_irp":kb_irp,"ok_isa":ok_isa,"ok_irp":ok_irp}
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



# ============================================================
# DB저축은행 공식 ISA Collector Adapter
# ============================================================

_DB_CACHE=None


def get_db_official():
    global _DB_CACHE

    if _DB_CACHE is None:
        _DB_CACHE=collect_db()

    return _DB_CACHE


def db_isa_official(bank,kind,cfg):
    result=get_db_official()
    item=result.get("ISA")

    if not isinstance(item,dict):
        o=blank(bank,kind,cfg,"fetch_or_parse_error")
        error=result.get("errors",{}).get(
            "ISA",
            "DB official collector returned no ISA data"
        )
        o["error"]=str(error)
        o["note"]=f"DB저축은행 공식 ISA API 수집 실패: {error}"
        return o

    o=blank(
        bank,
        kind,
        cfg,
        item.get("status","verified_official")
    )

    o["product"]=item.get("product_name") or cfg.get("product")
    o["rates"]=item.get(
        "rates",
        {f"{p}m":None for p in ISA_PERIODS}
    )
    o["source_url"]=item.get("source_url") or cfg.get("url")
    o["effective_date"]=item.get("effective_date")
    o["api_url"]=item.get("api_url")
    o["note"]=(
        "DB저축은행 공식 홈페이지 ISA 금리안내 API 자동수집. "
        f"기준일={item.get('effective_date') or '-'}"
    )

    return o



# ============================================================
# 공시일 / 시행일 표준화
# ============================================================

def normalize_date_value(value):
    """
    다양한 날짜 표기를 YYYY-MM-DD로 통일.
    지원:
    - 2026-08-03
    - 2026.08.03
    - 2026/08/03
    - 2026년 08월 03일
    """
    value=clean(value)

    if not value:
        return None

    patterns=[
        r"(\d{4})[-./](\d{1,2})[-./](\d{1,2})",
        r"(\d{4})\s*년\s*(\d{1,2})\s*월\s*(\d{1,2})\s*일",
    ]

    for pattern in patterns:
        m=re.search(pattern,value)

        if not m:
            continue

        y,mn,d=map(int,m.groups())

        return f"{y:04d}-{mn:02d}-{d:02d}"

    return None


def attach_disclosure_date(item):
    """
    기존 수집값은 그대로 유지하고
    disclosure_date / collected_at 표준 필드만 추가.

    우선순위:
    disclosure_date -> effective_date -> reference_date
    -> note 안 날짜 -> disclosure_sources 안 날짜
    """
    if not isinstance(item,dict):
        return item

    candidates=[
        item.get("disclosure_date"),
        item.get("effective_date"),
        item.get("reference_date"),
        item.get("note"),
    ]

    sources=item.get("disclosure_sources",[])

    if isinstance(sources,list):
        for source in sources:
            if not isinstance(source,dict):
                continue

            for key in (
                "disclosure_date",
                "effective_date",
                "reference_date",
                "date",
                "base_date",
                "rate_date",
            ):
                value=source.get(key)
                if value:
                    candidates.append(value)

    disclosure_date=None

    for candidate in candidates:
        normalized=normalize_date_value(candidate)

        if normalized:
            disclosure_date=normalized
            break

    item["disclosure_date"]=disclosure_date

    item["collected_at"]=(
        item.get("updated_at")
        or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    return item




# ============================================================
# v5.2 공시일 직접 탐색
# - 기존 금리 수집값은 절대 변경하지 않음
# - disclosure_date가 None인 경우에만 공식 화면에서 날짜 탐색
# - '기준일/시행일/적용일/변경일/공시일'과 가까운 날짜만 채택
# ============================================================

DISCLOSURE_PAGE_MAP={
    "우리금융":{
        "ISA":"https://www.woorisavingsbank.com/deposite-interest/view.do",
        "IRP":"https://www.woorisavingsbank.com/product/deposite/list.do",
    },
    "KB":{
        "ISA":"https://www.kbsavings.com/websquare/websquare.jsp?w2xPath=/jsp/depositItemInfo/depositItemInfo.xml&ITEM_CODE=IB13",
        "IRP":"https://www.kbsavings.com/websquare/websquare.jsp?w2xPath=/jsp/depositItemInfo/depositItemInfo.xml&ITEM_CODE=IB18",
    },
    "신한":{
        "ISA":"https://www.shinhansavings.com/PD_0080",
        "IRP":"https://www.shinhansavings.com/PD_0081",
    },
    "하나":{
        "ISA":"https://www.hanasavings.com/YPR/YPR0103",
        "IRP":"https://www.hanasavings.com/YPR/YPR0104",
    },
    "애큐온":{
        "ISA":"https://www.acuonsb.co.kr/sv_dpt1201170.act",
        "IRP":"https://www.acuonsb.co.kr/sv_dpt1201171.act",
    },
}

DATE_KEYWORDS=(
    "기준일",
    "기준 일",
    "시행일",
    "시행 일",
    "적용일",
    "적용 일",
    "변경일",
    "변경 일",
    "최종금리변경일",
    "금리변경일",
    "공시일",
    "공시 일",
    "고시일",
    "고시 일",
)

DATE_PATTERN=re.compile(
    r"(\d{4})\s*(?:[-./년]\s*)"
    r"(\d{1,2})\s*(?:[-./월]\s*)"
    r"(\d{1,2})\s*(?:일)?"
)


def strict_date_from_text(text):
    text=clean(text)

    if not text:
        return None

    candidates=[]

    for keyword in DATE_KEYWORDS:
        start=0

        while True:
            pos=text.find(keyword,start)

            if pos < 0:
                break

            left=max(0,pos-100)
            right=min(len(text),pos+len(keyword)+140)
            window=text[left:right]

            for m in DATE_PATTERN.finditer(window):
                try:
                    y,mn,d=map(int,m.groups())

                    if (
                        2000 <= y <= 2100
                        and 1 <= mn <= 12
                        and 1 <= d <= 31
                    ):
                        candidates.append(
                            f"{y:04d}-{mn:02d}-{d:02d}"
                        )
                except Exception:
                    pass

            start=pos+len(keyword)

    if not candidates:
        return None

    return max(candidates)


def fetch_disclosure_page_date(bank,category):
    url=(
        DISCLOSURE_PAGE_MAP
        .get(bank,{})
        .get(category)
    )

    if not url:
        return None,None

    try:
        html,final_url=fetch(url)
    except Exception:
        return None,url

    try:
        soup=BeautifulSoup(
            html,
            "html.parser"
        )
        text_value=" ".join(
            soup.stripped_strings
        )
    except Exception:
        text_value=html

    return (
        strict_date_from_text(
            text_value
        ),
        final_url,
    )


def enrich_disclosure_date(item):
    item=attach_disclosure_date(item)

    if not isinstance(item,dict):
        return item

    if item.get("disclosure_date"):
        item["disclosure_date_source"]="existing_collector"
        return item

    bank=clean(
        item.get("bank")
    )
    category=clean(
        item.get("category")
    ).upper()

    date_value,date_url=(
        fetch_disclosure_page_date(
            bank,
            category,
        )
    )

    if date_value:
        item["disclosure_date"]=date_value
        item["disclosure_date_source"]="official_page_keyword"
        item["disclosure_date_url"]=date_url
    else:
        item["disclosure_date_source"]="not_found"

        if date_url:
            item["disclosure_date_url"]=date_url

    return item



def main():
    mp=load(MAP)
    a=[]
    b=[]
    disclosure_banks=load_irp_disclosure()

    print("="*72)
    print("SBRateBot V5 ISA / IRP Collector v5.2 - Official + Disclosure Date Discovery")
    print("="*72)

    for i,(bank,cfg) in enumerate(mp["banks"].items(),1):

        # 한국투자:
        # 기존 성공 통합본은 그대로 유지하고,
        # 한국투자만 검증 완료된 Selenium/WebSquare 전용 수집기를 사용.
        if bank=="한국투자":
            try:
                ki=get_koreainvest_official(bank,cfg)
                x=ki["ISA"]
                y=ki["IRP"]
            except Exception as e:
                x=blank(bank,"isa",cfg["isa"],"fetch_or_parse_error")
                y=blank(bank,"irp",cfg["irp"],"fetch_or_parse_error")
                x["error"]=str(e)
                y["error"]=str(e)
                x["note"]=f"한국투자 공식 WebSquare 수집 실패: {e}"
                y["note"]=f"한국투자 공식 WebSquare 수집 실패: {e}"

        # OK:
        # ISA/IRP 모두 검증 완료된 공식 홈페이지 API를 사용.
        # 공식 API에서 제공하지 않는 기간을 과거 공시값으로 보충하지 않는다.
        elif bank=="OK":
            x=ok_isa(bank,"isa",cfg["isa"])
            y=ok_irp(bank,"irp",cfg["irp"])

        # DB:
        # ISA는 검증 완료된 DB 공식 홈페이지 API 사용.
        # IRP는 아직 공식 API 미통합이므로 기존 source-map 결과에
        # 사업자 공시 데이터를 fill-only 방식으로 병합한다.
        elif bank=="DB":
            x=db_isa_official(bank,"isa",cfg["isa"])
            y=one(bank,"irp",cfg["irp"])
            y=merge_irp_disclosure(
                bank,
                y,
                disclosure_banks
            )

        else:
            x=one(bank,"isa",cfg["isa"])
            y=one(bank,"irp",cfg["irp"])
            y=merge_irp_disclosure(
                bank,
                y,
                disclosure_banks
            )

        x=enrich_disclosure_date(x)
        y=enrich_disclosure_date(y)

        a.append(x)
        b.append(y)

        print(f"[{i}/{len(mp['banks'])}] {bank}")
        print(
            "  ISA:",
            x["rates"],
            f"[{x['status']}]"
        )
        print(
            "  IRP:",
            y["rates"],
            f"[{y['status']}]"
        )

    save(ISA,a)
    save(IRP,b)

    print("="*72)
    print("저장:",ISA)
    print("저장:",IRP)


if __name__=="__main__":
    main()
