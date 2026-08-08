# ==========================================
# SBRateBot V5
# Shinhan ISA / IRP Rate API Test v7
#
# v6 결과:
# /PD0080/selectSavPd.json, /PD0081/selectSavPd.json 로 직접 POST 시
# JSON 대신 SPA index.html 반환.
#
# v7:
# - /api prefix 포함 후보를 우선 테스트
# - JSON body / form body 둘 다 테스트
# - 먼저 상품 페이지 GET으로 쿠키 확보
# - Content-Type / 응답 앞부분을 판별
# - 성공한 JSON 응답에서 dscr10230.LIST 추출
# ==========================================

import json
import ssl
import urllib.request
import urllib.error
import http.cookiejar
from pathlib import Path
from urllib.parse import urlencode


BASE_URL = "https://www.shinhansavings.com"

TARGETS = {
    "ISA": {
        "page": "/PD_0080",
        "api_path": "/PD0080/selectSavPd.json",
        "pd_cd": 24014,
    },
    "IRP": {
        "page": "/PD_0081",
        "api_path": "/PD0081/selectSavPd.json",
        "pd_cd": 24015,
    },
}

OUTPUT = Path("data/shinhan_rate_api_test_v7.json")

SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE

COOKIE_JAR = http.cookiejar.CookieJar()

OPENER = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(COOKIE_JAR),
    urllib.request.HTTPSHandler(context=SSL_CONTEXT),
)

COMMON_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/142.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
}


def request(method, url, body=None, headers=None, timeout=60):
    all_headers = dict(COMMON_HEADERS)

    if headers:
        all_headers.update(headers)

    req = urllib.request.Request(
        url,
        data=body,
        headers=all_headers,
        method=method,
    )

    try:
        with OPENER.open(req, timeout=timeout) as response:
            raw = response.read()

            return {
                "ok": True,
                "status": getattr(response, "status", None),
                "url": response.geturl(),
                "headers": dict(response.headers.items()),
                "raw": raw,
                "text": raw.decode("utf-8", errors="replace"),
            }

    except urllib.error.HTTPError as error:
        raw = error.read()

        return {
            "ok": False,
            "status": error.code,
            "url": url,
            "headers": dict(error.headers.items()),
            "raw": raw,
            "text": raw.decode("utf-8", errors="replace"),
            "error": str(error),
        }

    except Exception as error:
        return {
            "ok": False,
            "status": None,
            "url": url,
            "headers": {},
            "raw": b"",
            "text": "",
            "error": str(error),
        }


def warmup(page):
    url = BASE_URL + page

    print("  [warmup GET]", url)

    result = request(
        "GET",
        url,
        headers={
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;"
                "q=0.9,*/*;q=0.8"
            ),
            "Referer": BASE_URL + "/",
        },
    )

    print(
        "    HTTP:",
        result["status"],
        "/ cookie count:",
        len(COOKIE_JAR),
    )

    return result


def classify_response(result):
    text = result.get("text", "").lstrip()
    ctype = result.get("headers", {}).get("Content-Type", "")

    if text.startswith("{") or text.startswith("["):
        return "json_like"

    if (
        text.lower().startswith("<!doctype html")
        or text.lower().startswith("<html")
    ):
        return "html"

    if "json" in ctype.lower():
        return "json_content_type"

    return "other"


def parse_json(result):
    text = result.get("text", "")

    try:
        return json.loads(text)
    except Exception:
        return None


def safe_get(obj, *keys):
    current = obj

    for key in keys:
        if not isinstance(current, dict):
            return None

        current = current.get(key)

        if current is None:
            return None

    return current


def normalize_row(row):
    if (
        isinstance(row, dict)
        and isinstance(row.get("map"), dict)
    ):
        return row["map"]

    return row if isinstance(row, dict) else {}


def extract_rate_rows(payload):
    if not isinstance(payload, dict):
        return [], {}

    data = payload.get("data", payload)

    rows = safe_get(
        data,
        "dscr10230",
        "LIST",
    )

    if not isinstance(rows, list):
        return [], {}

    normalized = []
    rates = {
        "3m": None,
        "6m": None,
        "12m": None,
        "24m": None,
        "36m": None,
    }

    for row in rows:
        item = normalize_row(row)

        term = item.get("TERM")
        rate = item.get("APPL_RATE")

        normalized.append(item)

        try:
            month = int(float(str(term).strip()))
            value = float(str(rate).strip())
        except Exception:
            continue

        key = f"{month}m"

        if key in rates:
            rates[key] = value

    return normalized, rates


def candidate_requests(cfg):
    api_path = cfg["api_path"]
    pd_cd = cfg["pd_cd"]

    endpoints = [
        "/api" + api_path,
        api_path,
    ]

    candidates = []

    for endpoint in endpoints:
        url = BASE_URL + endpoint

        json_body = json.dumps(
            {"PD_CD": pd_cd}
        ).encode("utf-8")

        form_body = urlencode(
            {"PD_CD": pd_cd}
        ).encode("utf-8")

        candidates.append({
            "name": "json",
            "url": url,
            "body": json_body,
            "headers": {
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json;charset=UTF-8",
                "Origin": BASE_URL,
                "Referer": BASE_URL + cfg["page"],
                "X-Requested-With": "XMLHttpRequest",
            },
        })

        candidates.append({
            "name": "form",
            "url": url,
            "body": form_body,
            "headers": {
                "Accept": "application/json, text/plain, */*",
                "Content-Type": (
                    "application/x-www-form-urlencoded; charset=UTF-8"
                ),
                "Origin": BASE_URL,
                "Referer": BASE_URL + cfg["page"],
                "X-Requested-With": "XMLHttpRequest",
            },
        })

    return candidates


def inspect(label, cfg):
    print()
    print("=" * 72)
    print(f"{label} API TEST v7")
    print("=" * 72)

    warmup(cfg["page"])

    attempts = []
    success = None

    for idx, candidate in enumerate(
        candidate_requests(cfg),
        start=1,
    ):
        print()
        print(
            f"  [{idx}] {candidate['name'].upper()} "
            f"{candidate['url']}"
        )

        result = request(
            "POST",
            candidate["url"],
            body=candidate["body"],
            headers=candidate["headers"],
        )

        kind = classify_response(result)
        payload = parse_json(result)

        rows, rates = (
            extract_rate_rows(payload)
            if payload is not None
            else ([], {})
        )

        print(
            "      HTTP:",
            result["status"],
        )
        print(
            "      Content-Type:",
            result["headers"].get("Content-Type"),
        )
        print(
            "      판별:",
            kind,
        )
        print(
            "      응답 길이:",
            len(result["text"]),
        )

        if payload is not None:
            print(
                "      JSON keys:",
                list(payload.keys())
                if isinstance(payload, dict)
                else type(payload).__name__,
            )

        if rows:
            print(
                "      dscr10230.LIST:",
                len(rows),
                "행",
            )
            print(
                "      금리:",
                rates,
            )

        attempt = {
            "request_type": candidate["name"],
            "url": candidate["url"],
            "http_status": result["status"],
            "response_type": kind,
            "content_type": result["headers"].get(
                "Content-Type"
            ),
            "response_length": len(result["text"]),
            "response_preview": result["text"][:1200],
            "json": payload,
            "rows": rows,
            "rates": rates,
        }

        attempts.append(attempt)

        if payload is not None and rows:
            success = attempt

            print()
            print("      >>> 공식 API 응답 확보")
            break

    return {
        "success": success is not None,
        "successful_attempt": success,
        "attempts": attempts,
    }


def main():
    print("=" * 72)
    print("SBRateBot V5 Shinhan ISA / IRP Rate API Test v7")
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
    print("최종 결과")
    print("=" * 72)

    for label, item in result.items():
        if item["success"]:
            success = item["successful_attempt"]

            print(label, "SUCCESS")
            print(
                "  URL:",
                success["url"],
            )
            print(
                "  TYPE:",
                success["request_type"],
            )
            print(
                "  RATES:",
                success["rates"],
            )
        else:
            print(label, "FAILED")

    print()
    print("저장:", OUTPUT)
    print()
    print(
        "※ 아직 isa_rates.json / irp_rates.json은 수정하지 않습니다."
    )


if __name__ == "__main__":
    main()
