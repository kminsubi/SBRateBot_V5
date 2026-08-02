# ============================================================
# SBRateBot V5 - OK Savings Bank ISA / IRP Official Collector
# crawler/ok.py
#
# Official source:
# https://www.oksavingsbank.com
#
# Product IDs:
#   ISA : 1261 (ISA정기예금)
#   IRP : 1237 (퇴직연금정기예금)
#
# Verified API:
#   POST /serviceEndpoint/httpService/request.json
#   application = OkbBeBiz
#   service     = SGdsDepsMang
#   operation   = getMaGdsDepsOne
#   grcmDvcd    = OKB
#   chnlDvcd    = HOM
#
# IMPORTANT:
# - This collector returns normalized values.
# - It does NOT overwrite the project's integrated ISA/IRP JSON by itself.
# - Import collect_ok() from the main collector and merge its result.
# ============================================================

import json
import re
import time
from datetime import datetime
from pathlib import Path

import requests


BASE_URL = "https://www.oksavingsbank.com"
API_URL = BASE_URL + "/serviceEndpoint/httpService/request.json"

SERVICE = "SGdsDepsMang"
OPERATION = "getMaGdsDepsOne"

PRODUCTS = {
    "ISA": {
        "depsGdsSqno": "1261",
        "expected_name": "ISA정기예금",
    },
    "IRP": {
        "depsGdsSqno": "1237",
        "expected_name": "퇴직연금정기예금",
    },
}

PERIOD_KEYS = ("3m", "6m", "12m", "24m", "36m")

TERM_MAP = {
    "3개월": "3m",
    "6개월": "6m",
    "12개월": "12m",
    "1년": "12m",
    "24개월": "24m",
    "2년": "24m",
    "36개월": "36m",
    "3년": "36m",
}


def new_session():
    session = requests.Session()

    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/142.0 Safari/537.36"
        ),
        "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
    })

    return session


def make_referer(seq):
    return (
        BASE_URL
        + "/#/gdsDepsMngmDtl"
        + f"?depsGdsSqno={seq}"
        + "&pageNo=2"
        + "&menuCd=00365"
        + "&mngmTr=00000"
        + "&inrtTp=00000"
        + "&etryMthd=00000"
        + "&acmlMthd=00000"
        + "&entrObjc=00000"
        + "&frdmEtryMthd=00000"
    )


def make_payload(seq):
    return {
        "header": {
            "application": "OkbBeBiz",
            "service": SERVICE,
            "operation": OPERATION,
            "appVer": None,
            "appVrsn": None,
            "authVl": None,
            "liveVrsn": None,
            "grcmDvcd": "OKB",
            "chnlDvcd": "HOM",
            "domainId": "www.oksavingsbank.com",
            "sessionId": "",
        },
        "data": {
            "depsGdsSqno": str(seq),
            "url": "/gdsDepsMngmList",
            "pageNo": 2,
            "menuCd": "00365",
        },
    }


def compact_json(obj):
    return json.dumps(
        obj,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")


def fetch_product(session, seq):
    # Warm-up creates the server-side session/JSESSIONID.
    session.get(
        BASE_URL + "/",
        timeout=30,
        allow_redirects=True,
    )

    response = session.post(
        API_URL,
        data=compact_json(make_payload(seq)),
        headers={
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": BASE_URL,
            "Referer": make_referer(seq),
            "Timestamp": str(int(time.time() * 1000)),
        },
        timeout=40,
        allow_redirects=True,
    )

    response.raise_for_status()

    body = response.json()

    header = body.get("header") or {}

    if str(header.get("rspnCd")) != "0":
        raise RuntimeError(
            "OK API error: "
            f"rspnCd={header.get('rspnCd')}, "
            f"msgCd={header.get('msgCd')}, "
            f"msgCont={header.get('msgCont')}"
        )

    detail = body.get("SMaGdsDeps01OutSubDto")

    if not isinstance(detail, dict):
        raise RuntimeError(
            "OK API response has no SMaGdsDeps01OutSubDto."
        )

    return detail


def parse_percent(text):
    if text is None:
        return None

    match = re.search(
        r"(-?\d+(?:\.\d+)?)\s*%",
        str(text),
    )

    if not match:
        return None

    return float(match.group(1))


def parse_irp_percent(text):
    """
    For retirement pension rows:
      DB 4.00% / DC,IRP 4.00%

    Prefer the DC/IRP rate. If the format changes, fall back to the
    first percentage in the row.
    """
    if text is None:
        return None

    value = str(text)

    patterns = [
        r"DC\s*,?\s*IRP\s*(-?\d+(?:\.\d+)?)\s*%",
        r"IRP\s*(-?\d+(?:\.\d+)?)\s*%",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            value,
            flags=re.IGNORECASE,
        )

        if match:
            return float(match.group(1))

    return parse_percent(value)


def parse_effective_date(inrt_list):
    for item in inrt_list:
        title = str(item.get("tl") or "").strip()
        cont = str(item.get("cont") or "").strip()

        if title:
            continue

        match = re.search(
            r"(\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2})",
            cont,
        )

        if match:
            year, month, day = match.groups()

            return (
                f"{int(year):04d}-"
                f"{int(month):02d}-"
                f"{int(day):02d}"
            )

    return None


def normalize_rates(product_type, detail):
    rates = {
        key: None
        for key in PERIOD_KEYS
    }

    inrt_list = detail.get("inrtGdList") or []

    for item in inrt_list:
        term = str(item.get("tl") or "").strip()
        cont = str(item.get("cont") or "").strip()

        key = TERM_MAP.get(term)

        if not key:
            continue

        if product_type == "IRP":
            rate = parse_irp_percent(cont)
        else:
            rate = parse_percent(cont)

        rates[key] = rate

    return rates, parse_effective_date(inrt_list)


def collect_one(session, product_type):
    config = PRODUCTS[product_type]

    detail = fetch_product(
        session,
        config["depsGdsSqno"],
    )

    product_name = str(
        detail.get("gdsNm") or ""
    ).strip()

    if (
        config["expected_name"]
        and product_name != config["expected_name"]
    ):
        raise RuntimeError(
            f"Unexpected OK product name: "
            f"{product_name!r} "
            f"(expected {config['expected_name']!r})"
        )

    rates, effective_date = normalize_rates(
        product_type,
        detail,
    )

    return {
        "bank": "OK",
        "product_type": product_type,
        "product_name": product_name,
        "rates": rates,
        "effective_date": effective_date,
        "source": "official",
        "status": "verified_official",
        "source_url": make_referer(
            config["depsGdsSqno"]
        ),
        "depsGdsSqno": config["depsGdsSqno"],
    }


def collect_ok():
    session = new_session()

    result = {
        "bank": "OK",
        "collected_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "ISA": None,
        "IRP": None,
        "errors": {},
    }

    for product_type in ("ISA", "IRP"):
        try:
            result[product_type] = collect_one(
                session,
                product_type,
            )

        except Exception as exc:
            result["errors"][product_type] = str(exc)

    return result


def compact_for_master(result):
    """
    Convenience representation for the existing 13-bank collector.

    Example:
      {
        "ISA": {"3m": 3.6, ...},
        "IRP": {"3m": None, ...}
      }
    """
    compact = {}

    for product_type in ("ISA", "IRP"):
        item = result.get(product_type)

        if item:
            compact[product_type] = item["rates"]
        else:
            compact[product_type] = {
                key: None
                for key in PERIOD_KEYS
            }

    return compact


def main():
    result = collect_ok()

    print("=" * 72)
    print("SBRateBot V5 - OK ISA / IRP Official Collector")
    print("=" * 72)

    for product_type in ("ISA", "IRP"):
        item = result.get(product_type)

        if item:
            print()
            print(
                f"{product_type}: "
                f"{item['product_name']}"
            )
            print(
                "  rates:",
                item["rates"],
            )
            print(
                "  effective_date:",
                item["effective_date"],
            )
            print(
                "  status:",
                item["status"],
            )
        else:
            print()
            print(
                f"{product_type}: ERROR - "
                f"{result['errors'].get(product_type)}"
            )

    # Debug/verification output only.
    # This does not replace the project's master data.
    output_path = Path(
        "data/ok_isa_irp_official.json"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print()
    print("saved:", output_path)

    if result["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
