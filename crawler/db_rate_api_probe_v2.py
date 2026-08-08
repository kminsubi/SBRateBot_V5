# -*- coding: utf-8 -*-
"""
DB저축은행 ISA / 퇴직연금 공식 금리 API Probe v2

목적
- DB저축은행 WebSquare 금리안내가 호출하는 공식 endpoint 직접 테스트
- /itb/dps/inr/selectDpstInrstGuidance.do
- 응답 원문을 저장해 다음 단계에서 ISA/IRP 금리 파서를 확정

실행:
    python db_rate_api_probe_v2.py
"""

import json
import re
from pathlib import Path

import requests


BASE = "https://www.idbsb.com"
PAGE_URL = BASE + "/w2/itb/dps/inr/dpstInrstGuidance.xml"
API_URL = BASE + "/itb/dps/inr/selectDpstInrstGuidance.do"

OUT_DIR = Path("data")
OUT_DIR.mkdir(exist_ok=True)

RAW_FILE = OUT_DIR / "db_rate_api_response_v2.txt"
SUMMARY_FILE = OUT_DIR / "db_rate_api_probe_v2.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/142.0.0.0 Safari/537.36"
    ),
    "Accept": "application/xml, text/xml, */*; q=0.01",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": PAGE_URL,
    "Origin": BASE,
    "X-Requested-With": "XMLHttpRequest",
}


def print_block(title, text, limit=5000):
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)
    print(text[:limit])
    if len(text) > limit:
        print(f"\n... truncated ({len(text):,} chars total)")


def extract_interesting(text):
    """응답에서 금리/ISA 관련 주변 문맥을 보기 쉽게 추출."""
    keywords = [
        "ds_inrstDtlIsaFdrmDpstList",
        "ds_inrstGoodsIsaFdrmDpst",
        "isaStdde",
        "intrtYy",
        "ernrtYy",
        "ISA",
        "퇴직",
        "IRP",
    ]

    hits = []
    lower = text.lower()

    for keyword in keywords:
        start = 0
        key_lower = keyword.lower()

        while True:
            idx = lower.find(key_lower, start)
            if idx < 0:
                break

            left = max(0, idx - 500)
            right = min(len(text), idx + 1500)
            chunk = text[left:right].strip()

            if chunk not in hits:
                hits.append(chunk)

            start = idx + len(keyword)

            if len(hits) >= 20:
                return hits

    return hits


def try_request(session, label, **kwargs):
    print(f"\n[{label}] POST {API_URL}")

    try:
        r = session.post(
            API_URL,
            headers=HEADERS,
            timeout=30,
            **kwargs,
        )

        print("HTTP:", r.status_code)
        print("Content-Type:", r.headers.get("Content-Type"))
        print("Length:", len(r.text))

        return r

    except Exception as e:
        print("ERROR:", repr(e))
        return None


def main():
    session = requests.Session()

    # ---------------------------------------------------------
    # 1. 먼저 공식 금리안내 XML을 열어 세션/쿠키 확보
    # ---------------------------------------------------------
    print("[1] Open official DB rate guidance page")

    try:
        page = session.get(
            PAGE_URL,
            headers={
                "User-Agent": HEADERS["User-Agent"],
                "Referer": BASE + "/",
            },
            timeout=30,
        )

        print("PAGE HTTP:", page.status_code)
        print("PAGE Length:", len(page.text))
        print("Cookies:", session.cookies.get_dict())

    except Exception as e:
        print("PAGE ERROR:", repr(e))

    # ---------------------------------------------------------
    # WebSquare ds_param 기본값
    #
    # 공식 XML에서 확인된 값:
    # ISA 금리구분 = 2
    # ISA 상품구분 = 01
    # ISA 예치금액 = 10,000,000
    # ---------------------------------------------------------
    ds_param = {
        "sn": "",
        "inrstFdrmDpstDsmn": "10000000",
        "inrstBilDsmn": "10000000",
        "inrstFdrmSvingsMtPaymntAmt": "100000",
        "inrstIsaFdrmDpstDsmn": "10000000",
        "inrstGoodsInrstSeFdrmDpst": "1",
        "inrstGoodsInrstSeBil": "1",
        "inrstGoodsInrstSeFdrmSvings": "1",
        "inrstGoodsInrstSeNrmltyDpst": "1",
        "inrstGoodsInrstSeIsaFdrmDpst": "2",
        "inrstGoodsGoodsSeFdrmDpst": "01",
        "inrstGoodsGoodsSeBil": "11",
        "inrstGoodsGoodsSeFdrmSvings": "21",
        "inrstGoodsGoodsSeNrmltyDpst": "31",
        "inrstGoodsGoodsSeIsaFdrmDpst": "01",
    }

    attempts = []

    # ---------------------------------------------------------
    # 2. WebSquare 계열에서 흔히 쓰는 JSON body
    # ---------------------------------------------------------
    payload_json = {
        "ds_param": ds_param
    }

    r = try_request(
        session,
        "JSON",
        json=payload_json,
    )

    if r is not None:
        attempts.append(("JSON", r))

    # ---------------------------------------------------------
    # 3. form + ds_param JSON 문자열
    # ---------------------------------------------------------
    payload_form = {
        "ds_param": json.dumps(ds_param, ensure_ascii=False)
    }

    r = try_request(
        session,
        "FORM-ds_param",
        data=payload_form,
    )

    if r is not None:
        attempts.append(("FORM-ds_param", r))

    # ---------------------------------------------------------
    # 4. WebSquare submission에서 자주 보이는 XML instance 형태
    # ---------------------------------------------------------
    xml_body = """<?xml version="1.0" encoding="UTF-8"?>
<map>
    <ds_param>
        <sn></sn>
        <inrstFdrmDpstDsmn>10000000</inrstFdrmDpstDsmn>
        <inrstBilDsmn>10000000</inrstBilDsmn>
        <inrstFdrmSvingsMtPaymntAmt>100000</inrstFdrmSvingsMtPaymntAmt>
        <inrstIsaFdrmDpstDsmn>10000000</inrstIsaFdrmDpstDsmn>
        <inrstGoodsInrstSeFdrmDpst>1</inrstGoodsInrstSeFdrmDpst>
        <inrstGoodsInrstSeBil>1</inrstGoodsInrstSeBil>
        <inrstGoodsInrstSeFdrmSvings>1</inrstGoodsInrstSeFdrmSvings>
        <inrstGoodsInrstSeNrmltyDpst>1</inrstGoodsInrstSeNrmltyDpst>
        <inrstGoodsInrstSeIsaFdrmDpst>2</inrstGoodsInrstSeIsaFdrmDpst>
        <inrstGoodsGoodsSeFdrmDpst>01</inrstGoodsGoodsSeFdrmDpst>
        <inrstGoodsGoodsSeBil>11</inrstGoodsGoodsSeBil>
        <inrstGoodsGoodsSeFdrmSvings>21</inrstGoodsGoodsSeFdrmSvings>
        <inrstGoodsGoodsSeNrmltyDpst>31</inrstGoodsGoodsSeNrmltyDpst>
        <inrstGoodsGoodsSeIsaFdrmDpst>01</inrstGoodsGoodsSeIsaFdrmDpst>
    </ds_param>
</map>
"""

    xml_headers = dict(HEADERS)
    xml_headers["Content-Type"] = "application/xml; charset=UTF-8"

    print(f"\n[XML] POST {API_URL}")

    try:
        r = session.post(
            API_URL,
            headers=xml_headers,
            data=xml_body.encode("utf-8"),
            timeout=30,
        )

        print("HTTP:", r.status_code)
        print("Content-Type:", r.headers.get("Content-Type"))
        print("Length:", len(r.text))

        attempts.append(("XML", r))

    except Exception as e:
        print("ERROR:", repr(e))

    # ---------------------------------------------------------
    # 5. 가장 유효해 보이는 응답 선택
    # ---------------------------------------------------------
    if not attempts:
        print("\nNo response.")
        return

    def response_score(item):
        label, response = item
        text = response.text

        score = 0

        if response.status_code == 200:
            score += 100

        for keyword in (
            "intrtYy",
            "isaStdde",
            "ds_inrstDtlIsaFdrmDpstList",
            "inrstDtlIsaFdrmDpst",
            "ISA",
        ):
            if keyword.lower() in text.lower():
                score += 100

        score += min(len(text) // 1000, 100)

        return score

    attempts.sort(
        key=response_score,
        reverse=True,
    )

    best_label, best = attempts[0]

    print()
    print("=" * 80)
    print("BEST RESPONSE")
    print("=" * 80)
    print("Method:", best_label)
    print("HTTP:", best.status_code)
    print("Length:", len(best.text))
    print("Content-Type:", best.headers.get("Content-Type"))

    # ---------------------------------------------------------
    # 6. 응답 원문 저장
    # ---------------------------------------------------------
    RAW_FILE.write_text(
        best.text,
        encoding="utf-8",
        errors="ignore",
    )

    print("RAW saved:", RAW_FILE)

    # ---------------------------------------------------------
    # 7. 중요 구간 출력
    # ---------------------------------------------------------
    hits = extract_interesting(best.text)

    if hits:
        for i, hit in enumerate(hits[:10], 1):
            print_block(
                f"INTERESTING #{i}",
                hit,
                3500,
            )
    else:
        print_block(
            "RAW RESPONSE PREVIEW",
            best.text,
            8000,
        )

    # ---------------------------------------------------------
    # 8. 숫자/기간 후보 간단 탐색
    # ---------------------------------------------------------
    rate_candidates = sorted(
        set(
            re.findall(
                r'(?<!\d)([0-9]{1,2}\.[0-9]{1,4})(?!\d)',
                best.text,
            )
        )
    )

    period_candidates = sorted(
        set(
            re.findall(
                r'(?<!\d)(3|6|12|24|36)(?!\d)',
                best.text,
            )
        ),
        key=lambda x: int(x),
    )

    print()
    print("=" * 80)
    print("CANDIDATES")
    print("=" * 80)
    print("periods:", period_candidates)
    print("rates:", rate_candidates[:100])

    summary = {
        "bank": "DB",
        "source": "official",
        "page_url": PAGE_URL,
        "api_url": API_URL,
        "best_method": best_label,
        "http_status": best.status_code,
        "content_type": best.headers.get("Content-Type"),
        "response_length": len(best.text),
        "period_candidates": period_candidates,
        "rate_candidates": rate_candidates,
        "raw_file": str(RAW_FILE),
    }

    SUMMARY_FILE.write_text(
        json.dumps(
            summary,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("SUMMARY saved:", SUMMARY_FILE)

    print()
    print("=" * 80)
    print("DONE")
    print("=" * 80)
    print("실행 결과 전체를 그대로 보내주세요.")
    print("특히 BEST RESPONSE / INTERESTING / CANDIDATES 부분이 중요합니다.")


if __name__ == "__main__":
    main()
