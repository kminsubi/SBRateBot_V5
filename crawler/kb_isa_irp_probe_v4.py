# ==========================================
# SBRateBot V5
# KB Savings ISA / IRP Focused Probe v4
#
# 목적:
# - KB저축은행 공식 사이트만 대상으로
#   ISA정기예금 / 퇴직연금 정기예금(DC형, IRP형) 관련
#   ITEM_CODE, 상세 XML, submission/action, 금리 endpoint를 좁혀 추적
# - 일반 대출/예금 잡음 최소화
# - 실제 금리 JSON은 수정하지 않음
# ==========================================

import json
import re
import ssl
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://www.kbsavings.com"
START = BASE + "/websquare/websquare.jsp?w2xPath=/jsp/main.xml"

OUT_JSON = Path("data/kb_isa_irp_probe_v4.json")
OUT_TXT = Path("data/kb_isa_irp_probe_v4.txt")
CACHE = Path("data/kb_isa_irp_probe_v4_cache")

TARGET_KEYWORDS = [
    "ISA정기예금",
    "ISA정기적금",
    "ISA",
    "퇴직연금 정기예금",
    "퇴직연금",
    "IRP",
    "DC형",
    "DC/IRP",
]

FOCUS_WORDS = [
    "depositItemInfo",
    "ITEM_CODE",
    "submission",
    "action",
    "service",
    ".do",
    ".json",
    "금리",
    "이율",
]

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def fetch(url, timeout=60):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/142 Safari/537.36"
            ),
            "Accept": "*/*",
            "Referer": BASE + "/",
        },
    )

    with urllib.request.urlopen(
        req,
        timeout=timeout,
        context=CTX,
    ) as r:
        raw = r.read()
        charset = r.headers.get_content_charset() or "utf-8"

        try:
            text = raw.decode(charset, errors="replace")
        except Exception:
            text = raw.decode("utf-8", errors="replace")

        return {
            "url": r.geturl(),
            "status": r.status,
            "content_type": r.headers.get("Content-Type", ""),
            "raw": raw,
            "text": text,
        }


def abs_url(base, value):
    return urllib.parse.urljoin(base, value)


def safe_name(url, index):
    p = urllib.parse.urlparse(url)
    name = Path(p.path).name or "index"

    if p.query:
        name += "_" + re.sub(
            r"[^A-Za-z0-9._-]+",
            "_",
            p.query,
        )[:80]

    return f"{index:03d}_" + re.sub(
        r"[^A-Za-z0-9._-]+",
        "_",
        name,
    )


def get_contexts(text, keyword, radius=700, limit=20):
    out = []
    low = text.lower()
    key = keyword.lower()
    pos = 0

    while len(out) < limit:
        idx = low.find(key, pos)

        if idx < 0:
            break

        out.append(
            text[
                max(0, idx - radius):
                min(len(text), idx + len(keyword) + radius)
            ].replace("\r", " ").replace("\n", " ")
        )

        pos = idx + len(keyword)

    return out


def extract_item_codes(text):
    out = []

    patterns = [
        r'ITEM_CODE\s*=\s*([A-Za-z0-9_-]+)',
        r'ITEM_CODE=([A-Za-z0-9_-]+)',
        r'["\']ITEM_CODE["\']\s*[:=]\s*["\']?([A-Za-z0-9_-]+)',
    ]

    for pattern in patterns:
        for m in re.finditer(pattern, text, flags=re.I):
            code = m.group(1)

            ctx = text[
                max(0, m.start() - 500):
                min(len(text), m.end() + 1200)
            ].replace("\r", " ").replace("\n", " ")

            out.append({
                "item_code": code,
                "context": ctx,
            })

    # dedupe
    seen = set()
    result = []

    for item in out:
        key = item["item_code"] + "|" + item["context"]

        if key not in seen:
            seen.add(key)
            result.append(item)

    return result


def extract_deposit_item_urls(text):
    out = set()

    patterns = [
        r'["\']([^"\']*depositItemInfo[^"\']*)["\']',
        r'["\']([^"\']*depositItemInfoMain[^"\']*)["\']',
    ]

    for pattern in patterns:
        for value in re.findall(pattern, text, flags=re.I):
            if value.startswith(("javascript:", "data:")):
                continue

            if value.startswith("http"):
                out.add(value)
            else:
                out.add(abs_url(BASE + "/", value))

    return sorted(out)


def extract_submission_contexts(text):
    out = []

    for keyword in FOCUS_WORDS:
        for ctx in get_contexts(
            text,
            keyword,
            radius=900,
            limit=30,
        ):
            out.append({
                "keyword": keyword,
                "context": ctx,
            })

    return out


def extract_api_candidates(text):
    out = set()

    patterns = [
        r'["\']([^"\']+\.(?:do|json)(?:\?[^"\']*)?)["\']',
        r'["\']((?:/|https?://)[^"\']*(?:rate|intr|interest|deposit|saving|goods|prod|item)[^"\']*)["\']',
    ]

    for pattern in patterns:
        for value in re.findall(pattern, text, flags=re.I):
            if len(value) > 500:
                continue

            if value.startswith(("javascript:", "data:")):
                continue

            out.add(
                value if value.startswith("http")
                else abs_url(BASE + "/", value)
            )

    return sorted(out)


def inspect(url):
    r = fetch(url)

    keyword_hits = {}

    for kw in TARGET_KEYWORDS:
        ctxs = get_contexts(
            r["text"],
            kw,
            radius=700,
            limit=20,
        )

        if ctxs:
            keyword_hits[kw] = ctxs

    return {
        "url": r["url"],
        "status": r["status"],
        "content_type": r["content_type"],
        "size": len(r["raw"]),
        "keyword_hits": keyword_hits,
        "item_codes": extract_item_codes(r["text"]),
        "deposit_item_urls": extract_deposit_item_urls(r["text"]),
        "api_candidates": extract_api_candidates(r["text"]),
        "submission_contexts": extract_submission_contexts(r["text"]),
        "_raw": r["raw"],
    }


def target_score(item):
    score = 0
    hits = item.get("keyword_hits", {})

    if "ISA정기예금" in hits:
        score += 10
    if "퇴직연금 정기예금" in hits:
        score += 10
    if "퇴직연금" in hits:
        score += 5
    if "IRP" in hits:
        score += 5
    if "DC형" in hits:
        score += 3

    if item.get("item_codes"):
        score += 5

    if item.get("deposit_item_urls"):
        score += 5

    return score


def main():
    print("=" * 84)
    print("SBRateBot V5 KB Savings ISA / IRP Focused Probe v4")
    print("=" * 84)

    CACHE.mkdir(
        parents=True,
        exist_ok=True,
    )

    queue = [START]
    seen = set()
    pages = []
    errors = []

    max_pages = 45

    while queue and len(seen) < max_pages:
        url = queue.pop(0)

        if url in seen:
            continue

        seen.add(url)

        try:
            item = inspect(url)
            score = target_score(item)

            print(
                f"[{len(seen):02d}] "
                f"score={score:02d} "
                f"{item['status']} "
                f"{item['size']:,}B "
                f"{item['url']}"
            )

            cache_file = CACHE / safe_name(
                item["url"],
                len(seen),
            )
            cache_file.write_bytes(item["_raw"])

            item["cache_file"] = str(cache_file)
            item.pop("_raw")

            pages.append(item)

            next_urls = set(
                item.get("deposit_item_urls", [])
                + item.get("api_candidates", [])
            )

            for nxt in sorted(next_urls):
                if "kbsavings.com" not in nxt:
                    continue

                low = nxt.lower()

                if (
                    "deposititeminfo" in low
                    or ".xml" in low
                    or ".do" in low
                    or ".jsp" in low
                ):
                    if (
                        nxt not in seen
                        and nxt not in queue
                    ):
                        queue.append(nxt)

        except Exception as e:
            print("     FAIL:", e)

            errors.append({
                "url": url,
                "error": repr(e),
            })

    # 상품 관련 페이지만 추림
    focused = [
        item
        for item in pages
        if target_score(item) > 0
    ]

    focused.sort(
        key=target_score,
        reverse=True,
    )

    result = {
        "start": START,
        "focused_pages": focused,
        "all_item_codes": [],
        "all_deposit_item_urls": [],
        "all_api_candidates": [],
        "errors": errors,
    }

    all_codes = []
    all_deposit_urls = set()
    all_api = set()

    for item in focused:
        for code in item.get("item_codes", []):
            all_codes.append({
                "source": item["url"],
                **code,
            })

        all_deposit_urls.update(
            item.get("deposit_item_urls", [])
        )

        all_api.update(
            item.get("api_candidates", [])
        )

    result["all_item_codes"] = all_codes
    result["all_deposit_item_urls"] = sorted(
        all_deposit_urls
    )
    result["all_api_candidates"] = sorted(
        all_api
    )

    OUT_JSON.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUT_JSON.write_text(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    lines = [
        "=" * 100,
        "SBRateBot V5 KB Savings ISA / IRP Focused Probe v4",
        "=" * 100,
        "",
        "START: " + START,
        "",
    ]

    for item in focused:
        lines += [
            "-" * 100,
            f"SCORE={target_score(item)}",
            item["url"],
            "-" * 100,
        ]

        for kw, ctxs in item.get(
            "keyword_hits",
            {},
        ).items():
            lines.append(
                f"[KEYWORD] {kw}"
            )

            for ctx in ctxs[:8]:
                lines.append(
                    "  " + ctx[:2200]
                )

        if item.get("item_codes"):
            lines.append("[ITEM CODES]")

            for code in item["item_codes"][:50]:
                lines.append(
                    f"  {code['item_code']}"
                )
                lines.append(
                    "    " + code["context"][:1800]
                )

        if item.get("deposit_item_urls"):
            lines.append("[DEPOSIT ITEM URLS]")

            for url in item["deposit_item_urls"][:80]:
                lines.append(
                    "  " + url
                )

        if item.get("api_candidates"):
            lines.append("[API CANDIDATES]")

            for url in item["api_candidates"][:120]:
                lines.append(
                    "  " + url
                )

        if item.get("submission_contexts"):
            lines.append("[SUBMISSION/ACTION CONTEXTS]")

            for sub in item["submission_contexts"][:80]:
                # ISA/IRP/ITEM_CODE/depositItemInfo 포함 문맥만 출력
                low = sub["context"].lower()

                if any(
                    x.lower() in low
                    for x in (
                        "isa",
                        "퇴직연금",
                        "irp",
                        "dc형",
                        "item_code",
                        "deposititeminfo",
                    )
                ):
                    lines.append(
                        f"  ({sub['keyword']}) "
                        + sub["context"][:2200]
                    )

        lines.append("")

    lines += [
        "=" * 100,
        "ALL ITEM CODES",
        "=" * 100,
    ]

    for item in all_codes:
        lines.append(
            f"{item['item_code']} | "
            f"{item['source']}"
        )
        lines.append(
            "  " + item["context"][:1400]
        )

    lines += [
        "",
        "=" * 100,
        "ALL DEPOSIT ITEM URLS",
        "=" * 100,
    ]
    lines.extend(
        result["all_deposit_item_urls"]
    )

    lines += [
        "",
        "=" * 100,
        "ALL API CANDIDATES",
        "=" * 100,
    ]
    lines.extend(
        result["all_api_candidates"]
    )

    OUT_TXT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print()
    print("=" * 84)
    print("탐색 완료")
    print("=" * 84)
    print("Focused pages:", len(focused))
    print("ITEM_CODE candidates:", len(all_codes))
    print("Deposit URLs:", len(result["all_deposit_item_urls"]))
    print("API candidates:", len(result["all_api_candidates"]))
    print()
    print("JSON:", OUT_JSON)
    print("TXT :", OUT_TXT)
    print("※ KB저축은행 ISA/IRP 전용 탐색 / 실제 금리 JSON 미수정")


if __name__ == "__main__":
    main()
