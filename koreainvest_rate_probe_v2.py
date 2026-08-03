# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse
import requests

BASE = "https://sb.koreainvestment.com"
TARGETS = {
    "ISA": BASE + "/?PRD-PDS001-10#",
    "IRP": BASE + "/?PRD-PDS001-11#",
}
OUT_JSON = Path("data/koreainvest_rate_probe_v2.json")
OUT_TXT = Path("data/koreainvest_rate_probe_v2.txt")

S = requests.Session()
S.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/142.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
})

SIGNALS = [
    "intrGridView", "금리안내", "금리", "이율", "interest", "rate",
    "PRD-PDS001-10", "PRD-PDS001-11", "ISA", "IRP", "퇴직연금",
    "submission", "submit", "service", "transaction", "ajax", "fetch(",
    "$.ajax", ".do", ".xml", ".json", ".wq", "WebSquare", "dataList"
]

URL_PATTERNS = [
    r"[\"']([^\"']+\.(?:js|xml|json|jsp|do|wq)(?:\?[^\"']*)?)[\"']",
    r"(?:src|href)\s*=\s*[\"']([^\"']+)[\"']",
    r"(?:url|action|src|href)\s*[:=]\s*[\"']([^\"']+)[\"']",
]


def fetch(url, referer=None):
    headers = {}
    if referer:
        headers["Referer"] = referer
    r = S.get(url, headers=headers, timeout=35, allow_redirects=True)
    if not r.encoding or r.encoding.lower() == "iso-8859-1":
        r.encoding = r.apparent_encoding or "utf-8"
    return r


def normalize_url(value, base_url):
    value = (value or "").strip()
    if not value or value.startswith(("javascript:", "mailto:", "tel:", "#", "data:")):
        return None
    try:
        url = urljoin(base_url, value)
        p = urlparse(url)
        if p.netloc and p.netloc != "sb.koreainvestment.com":
            return None
        return url
    except Exception:
        return None


def extract_urls(text, base_url):
    found = set()
    for pat in URL_PATTERNS:
        for m in re.finditer(pat, text, flags=re.I):
            u = normalize_url(m.group(1), base_url)
            if u:
                found.add(u)
    return sorted(found)


def signal_score(text, url=""):
    low = text.lower()
    weights = {
        "intrgridview": 220, "prd-pds001-10": 180, "prd-pds001-11": 180,
        "금리안내": 150, "금리": 60, "이율": 60, "퇴직연금": 80,
        "isa": 35, "irp": 35, "submission": 80, "transaction": 70,
        "service": 25, ".do": 45, ".xml": 45, ".json": 35, ".wq": 35,
        "ajax": 30, "fetch(": 30, "datalist": 50, "websquare": 15,
    }
    score = sum(min(low.count(k), 12) * v for k, v in weights.items())
    if any(x in url.lower() for x in ("prd", "pds", "websquare", "xml", "js")):
        score += 30
    return score


def contexts(text, max_hits=24):
    low = text.lower()
    rows = []
    used = []
    for sig in SIGNALS:
        start = 0
        while True:
            pos = low.find(sig.lower(), start)
            if pos < 0:
                break
            if all(abs(pos - old) > 300 for old in used):
                a = max(0, pos - 700)
                b = min(len(text), pos + 1800)
                rows.append({"signal": sig, "position": pos, "context": text[a:b]})
                used.append(pos)
                if len(rows) >= max_hits:
                    return rows
            start = pos + max(1, len(sig))
    return rows


def is_noise(url):
    low = url.lower().split("?", 1)[0]
    return low.endswith((".css", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".woff", ".woff2", ".ttf", ".map"))


def main():
    print("=" * 96)
    print("SBRateBot V5 - 한국투자저축은행 WebSquare 금리 호출 Probe v2")
    print("=" * 96)

    result = {"bank": "한국투자", "targets": TARGETS, "pages": {}, "candidates": []}
    queue = []
    seen = set()

    for kind, url in TARGETS.items():
        print(f"\n[PAGE] {kind} {url}")
        try:
            r = fetch(url)
            text = r.text
            print("HTTP:", r.status_code, "SIZE:", len(r.content), "FINAL:", r.url)
            result["pages"][kind] = {
                "url": url,
                "final_url": r.url,
                "status": r.status_code,
                "size": len(r.content),
                "content_type": r.headers.get("Content-Type"),
                "cookies": S.cookies.get_dict(),
                "signals": contexts(text, 12),
            }
            for u in extract_urls(text, r.url):
                if not is_noise(u):
                    queue.append((u, r.url, 0))
        except Exception as e:
            print("ERROR:", repr(e))
            result["pages"][kind] = {"url": url, "error": repr(e)}

    for u in (
        BASE + "/websquare/configPcw.js?ver=20260611",
        BASE + "/websquare/javascript.wq?q=/bootloader",
    ):
        queue.append((u, TARGETS["ISA"], 0))

    inspected = []
    fetched = 0
    max_fetch = 90

    while queue and fetched < max_fetch:
        url, referer, depth = queue.pop(0)
        if url in seen or is_noise(url):
            continue
        seen.add(url)
        fetched += 1

        try:
            r = fetch(url, referer)
            text = r.text
            score = signal_score(text, r.url)
            hits = contexts(text, 18)
            discovered = []

            for u in extract_urls(text, r.url):
                if is_noise(u):
                    continue
                discovered.append(u)
                if depth < 1 and u not in seen:
                    queue.append((u, r.url, depth + 1))

            if score > 0 or hits:
                inspected.append({
                    "url": r.url,
                    "status": r.status_code,
                    "content_type": r.headers.get("Content-Type"),
                    "size": len(r.content),
                    "score": score,
                    "signals": hits,
                    "discovered_urls": discovered[:80],
                })
                print(f"[{fetched:02d}] HTTP {r.status_code} SCORE {score:4d} {r.url}")

        except Exception as e:
            if any(x in url.lower() for x in ("prd", "pds", "websquare", ".js", ".xml", ".do", ".wq")):
                inspected.append({"url": url, "error": repr(e), "score": 0})
                print(f"[{fetched:02d}] ERROR {url} -> {e!r}")

    inspected.sort(key=lambda x: x.get("score", 0), reverse=True)
    result["candidates"] = inspected

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "=" * 120,
        "SBRateBot V5 한국투자저축은행 WebSquare 금리 호출 Probe v2",
        "=" * 120,
        "ISA=PRD-PDS001-10",
        "IRP=PRD-PDS001-11",
        "목표=intrGridView에 금리 데이터를 넣는 실제 호출/API 후보 찾기",
        "",
    ]

    for kind in ("ISA", "IRP"):
        page = result["pages"].get(kind, {})
        lines += [
            "-" * 120,
            f"{kind} PAGE",
            f"URL={page.get('url')}",
            f"FINAL={page.get('final_url')}",
            f"HTTP={page.get('status')}",
            f"SIZE={page.get('size')}",
        ]
        if page.get("error"):
            lines.append("ERROR=" + page["error"])
        for hit in page.get("signals", []):
            lines += ["", f">>> {hit['signal']} @ {hit['position']}", hit["context"]]

    lines += ["", "=" * 120, "TOP CANDIDATES", "=" * 120]

    for i, item in enumerate(inspected[:30], 1):
        lines += [
            "",
            "-" * 120,
            f"CANDIDATE #{i}",
            f"SCORE={item.get('score', 0)}",
            f"URL={item.get('url')}",
            f"HTTP={item.get('status')}",
            f"TYPE={item.get('content_type')}",
            f"SIZE={item.get('size')}",
        ]
        if item.get("error"):
            lines.append("ERROR=" + item["error"])
            continue
        for hit in item.get("signals", [])[:12]:
            lines += ["", f">>> {hit['signal']} @ {hit['position']}", hit["context"]]
        urls = item.get("discovered_urls", [])[:25]
        if urls:
            lines += ["", "[DISCOVERED URLS]"] + urls

    OUT_TXT.write_text("\n".join(lines), encoding="utf-8")

    print("\n완료")
    print("JSON:", OUT_JSON)
    print("TXT :", OUT_TXT)
    print("보내줄 파일: data/koreainvest_rate_probe_v2.txt")
    print("기존 ISA/IRP JSON은 수정하지 않습니다.")


if __name__ == "__main__":
    main()
