# ==========================================
# SBRateBot V5
# Shinhan ISA / IRP Rate API Test v6
#
# 확인된 공식 API:
# ISA: POST /PD0080/selectSavPd.json  PD_CD=24014
# IRP: POST /PD0081/selectSavPd.json  PD_CD=24015
#
# 목적:
# - 실제 API 직접 호출
# - dscr10230.LIST 전체 구조 출력
# - TERM / APPL_RATE 기준 기간별 금리 후보 추출
# - JSON 파일은 아직 수정하지 않음
# ==========================================

import json
import ssl
import urllib.request
from pathlib import Path
from urllib.parse import urlencode


BASE_URL = "https://www.shinhansavings.com"

TARGETS = {
    "ISA": {
        "endpoint": "/PD0080/selectSavPd.json",
        "pd_cd": "24014",
    },
    "IRP": {
        "endpoint": "/PD0081/selectSavPd.json",
        "pd_cd": "24015",
    },
}

OUTPUT = Path("data/shinhan_rate_api_test_v6.json")

SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE


def post_form(url, data, timeout=60):
    body = urlencode(data).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/142.0 Safari/537.36"
            ),
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": BASE_URL,
            "Referer": BASE_URL + "/",
            "X-Requested-With": "XMLHttpRequest",
        },
        method="POST",
    )

    with urllib.request.urlopen(
        req,
        timeout=timeout,
        context=SSL_CONTEXT,
    ) as response:
        raw = response.read()
        text = raw.decode("utf-8", errors="replace")

        return {
            "status": getattr(response, "status", None),
            "headers": dict(response.headers.items()),
            "text": text,
        }


def safe_get(obj, *keys):
    cur = obj

    for key in keys:
        if not isinstance(cur, dict):
            return None

        cur = cur.get(key)

        if cur is None:
            return None

    return cur


def normalize_row(row):
    if isinstance(row, dict) and "map" in row and isinstance(row["map"], dict):
        return row["map"]

    if isinstance(row, dict):
        return row

    return {}


def extract_rates(rows):
    result = {
        "3m": None,
        "6m": None,
        "12m": None,
        "24m": None,
        "36m": None,
    }

    normalized = []

    for row in rows or []:
        data = normalize_row(row)

        term = data.get("TERM")
        rate = data.get("APPL_RATE")

        normalized.append({
            "TERM": term,
            "APPL_RATE": rate,
            "raw": data,
        })

        try:
            months = int(float(str(term).strip()))
        except Exception:
            continue

        try:
            value = float(str(rate).strip())
        except Exception:
            continue

        key = f"{months}m"

        if key in result:
            result[key] = value

    return result, normalized


def inspect(label, cfg):
    url = BASE_URL + cfg["endpoint"]

    print()
    print("=" * 72)
    print(f"{label} API TEST")
    print("=" * 72)
    print("URL   :", url)
    print("PD_CD :", cfg["pd_cd"])

    try:
        response = post_form(
            url,
            {
                "PD_CD": cfg["pd_cd"],
            },
        )

    except Exception as error:
        print("요청 실패:", error)

        return {
            "success": False,
            "error": str(error),
        }

    print("HTTP  :", response["status"])

    text = response["text"]

    print("응답 길이:", len(text))

    try:
        payload = json.loads(text)

    except Exception as error:
        print("JSON 파싱 실패:", error)
        print()
        print("[응답 앞부분]")
        print(text[:3000])

        return {
            "success": False,
            "http_status": response["status"],
            "error": "json_parse_failed",
            "response_preview": text[:5000],
        }

    data = payload.get("data", payload)

    rows = safe_get(
        data,
        "dscr10230",
        "LIST",
    )

    print()
    print("[dscr10230.LIST]")

    if isinstance(rows, list):
        print("행 개수:", len(rows))

        for idx, row in enumerate(rows, 1):
            print(f"{idx:02d}. {row}")

    else:
        print("LIST 없음 또는 예상과 다른 구조")
        print("data keys:", list(data.keys()) if isinstance(data, dict) else type(data))

    rates, normalized = extract_rates(
        rows if isinstance(rows, list) else []
    )

    print()
    print("[기간별 금리 후보]")
    print(rates)

    print()
    print("[selectSavPd]")
    print(
        json.dumps(
            data.get("selectSavPd"),
            ensure_ascii=False,
            indent=2,
        )[:5000]
        if isinstance(data, dict)
        else None
    )

    print()
    print("[selectPdDescDo]")
    print(
        json.dumps(
            data.get("selectPdDescDo"),
            ensure_ascii=False,
            indent=2,
        )[:5000]
        if isinstance(data, dict)
        else None
    )

    return {
        "success": True,
        "http_status": response["status"],
        "endpoint": cfg["endpoint"],
        "pd_cd": cfg["pd_cd"],
        "rates": rates,
        "normalized_rows": normalized,
        "raw_payload": payload,
    }


def main():
    print("=" * 72)
    print("SBRateBot V5 Shinhan ISA / IRP Rate API Test v6")
    print("=" * 72)

    result = {}

    for label, cfg in TARGETS.items():
        result[label] = inspect(
            label,
            cfg,
        )

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT.write_text(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print()
    print("=" * 72)
    print("최종 요약")
    print("=" * 72)

    for label, item in result.items():
        print(
            label,
            "->",
            item.get("rates")
            if item.get("success")
            else item.get("error")
        )

    print()
    print("저장:", OUTPUT)
    print()
    print("※ 테스트 버전입니다.")
    print("※ isa_rates.json / irp_rates.json은 아직 수정하지 않습니다.")


if __name__ == "__main__":
    main()
