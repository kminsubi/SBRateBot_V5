# -*- coding: utf-8 -*-
"""
DB저축은행 WebSquare Submission Probe v3

v2 결과:
- 공식 endpoint는 HTTP 200 도달
- itb.valid.error.0003 = 필수 입력정보 누락
- 즉 URL 문제보다 "WebSquare submission 직렬화 형식" 문제로 좁혀짐

v1 소스에서 확인:
- ajaxLib.DEFAULT_OPTIONS_MEDIATYPE = application/json
- ref = data:json, [{"id":"ds_param","key":"ds_param","action":"all"}]
- action = /itb/dps/inr/selectDpstInrstGuidance.do

v3 목표:
- WebSquare가 보낼 가능성이 높은 JSON envelope들을 순차 테스트
- 유효 응답(intrtYy / isaStdde / ds_inrst...)이 나오면 즉시 저장
"""

import json
from pathlib import Path
import requests

BASE = "https://www.idbsb.com"
PAGE = BASE + "/w2/itb/dps/inr/dpstInrstGuidance.xml"
API = BASE + "/itb/dps/inr/selectDpstInrstGuidance.do"

OUT = Path("data/db_websquare_submission_probe_v3.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

S = requests.Session()
S.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/142.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Origin": BASE,
    "Referer": PAGE,
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json;charset=UTF-8",
})

DS_PARAM = {
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

TARGET_KEYS = (
    "intrtYy",
    "isaStdde",
    "ds_inrst",
    "ds_inrstGoodsIsaFdrmDpst",
    "ds_inrstDtlIsaFdrmDpstList",
)

def score(text):
    s = 0
    low = text.lower()
    for k in TARGET_KEYS:
        if k.lower() in low:
            s += 1000
    if "errorcode" not in low:
        s += 100
    s += min(len(text), 100000) // 100
    return s

def variants():
    ref_meta = [{
        "id": "ds_param",
        "key": "ds_param",
        "action": "all",
    }]

    # 핵심은 nested/flat + WebSquare envelope 조합 비교
    return [
        ("nested_ds_param", {
            "ds_param": DS_PARAM,
        }),
        ("flat_fields", {
            **DS_PARAM,
        }),
        ("data_nested", {
            "data": {
                "ds_param": DS_PARAM,
            }
        }),
        ("request_nested", {
            "request": {
                "ds_param": DS_PARAM,
            }
        }),
        ("body_nested", {
            "body": {
                "ds_param": DS_PARAM,
            }
        }),
        ("websquare_ref_data", {
            "ref": ref_meta,
            "data": {
                "ds_param": DS_PARAM,
            }
        }),
        ("websquare_ref_direct", {
            "ref": ref_meta,
            "ds_param": DS_PARAM,
        }),
        ("submission_envelope_1", {
            "id": "fnDpstInrstGuidance",
            "ref": ref_meta,
            "data": {
                "ds_param": DS_PARAM,
            }
        }),
        ("submission_envelope_2", {
            "submissionId": "fnDpstInrstGuidance",
            "ref": ref_meta,
            "data": {
                "ds_param": DS_PARAM,
            }
        }),
        ("submission_envelope_3", {
            "_submissionId": "fnDpstInrstGuidance",
            "ref": ref_meta,
            "data": {
                "ds_param": DS_PARAM,
            }
        }),
        # sn이 validation 필수일 가능성도 별도 점검
        ("nested_sn_1", {
            "ds_param": {
                **DS_PARAM,
                "sn": "1",
            }
        }),
        ("flat_sn_1", {
            **DS_PARAM,
            "sn": "1",
        }),
    ]

def main():
    print("=" * 88)
    print("DB Savings Bank WebSquare Submission Probe v3")
    print("=" * 88)

    # warmup
    try:
        r = S.get(PAGE, timeout=30)
        print("PAGE:", r.status_code, "len=", len(r.text))
        print("cookies:", S.cookies.get_dict())
    except Exception as e:
        print("PAGE ERROR:", repr(e))

    results = []

    for name, payload in variants():
        print()
        print("[TEST]", name)

        try:
            r = S.post(
                API,
                data=json.dumps(
                    payload,
                    ensure_ascii=False,
                    separators=(",", ":"),
                ).encode("utf-8"),
                timeout=30,
            )

            text = r.text
            sc = score(text)

            print(" HTTP:", r.status_code)
            print(" LEN :", len(text))
            print(" SCORE:", sc)
            print(" HEAD:", text[:500])

            results.append({
                "name": name,
                "status": r.status_code,
                "content_type": r.headers.get("Content-Type"),
                "length": len(text),
                "score": sc,
                "payload": payload,
                "response": text,
            })

        except Exception as e:
            print(" ERROR:", repr(e))
            results.append({
                "name": name,
                "error": repr(e),
            })

    results.sort(
        key=lambda x: x.get("score", -1),
        reverse=True,
    )

    OUT.write_text(
        json.dumps(
            {
                "api": API,
                "page": PAGE,
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print()
    print("=" * 88)
    print("BEST")
    print("=" * 88)

    if results:
        best = results[0]
        print("name :", best.get("name"))
        print("score:", best.get("score"))
        print("HTTP :", best.get("status"))
        print("response:")
        print(best.get("response", "")[:10000])

    print()
    print("saved:", OUT)
    print()
    print("이 JSON 파일을 보내주세요:")
    print("data/db_websquare_submission_probe_v3.json")


if __name__ == "__main__":
    main()
