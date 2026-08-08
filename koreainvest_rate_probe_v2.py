# -*- coding: utf-8 -*-
"""
SBRateBot V5 - 한국투자저축은행 WebSquare Route Probe v2
ISA: PRD-PDS001-10
IRP: PRD-PDS001-11

실행:
    python koreainvest_rate_probe_v2.py

출력:
    koreainvest_rate_probe_v2.txt
"""

import re
import sys
import time
from urllib.parse import urljoin
import requests

BASE = "https://sb.koreainvestment.com/"
TARGETS = {
    "ISA": "https://sb.koreainvestment.com/?PRD-PDS001-10#",
    "IRP": "https://sb.koreainvestment.com/?PRD-PDS001-11#",
}
OUT = "koreainvest_rate_probe_v2.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/142.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
    "Referer": BASE,
}
session = requests.Session()
session.headers.update(HEADERS)

KEYWORDS = [
    "PRD-PDS001-10", "PRD-PDS001-11", "PRD-PDS001",
    "w2xPath", "welcome-file", "submission", "submit",
    "action", ".do", ".xml", ".w5", "ajax",
    "rate", "금리", "금리안내", "ISA", "퇴직연금"
]

RESOURCE_RE = re.compile("(?:src|href)\\s*=\\s*[\"']([^\"'#]+)[\"']", re.I)
URLISH_RE = re.compile("[\"']([^\"']+\\.(?:xml|w5|js|json|do|wq)(?:\\?[^\"']*)?)[\"']", re.I)


def log(fp, text=""):
    print(text)
    fp.write(str(text) + "\n")
    fp.flush()


def divider(fp, title=""):
    log(fp, "\n" + "=" * 110)
    if title:
        log(fp, title)
        log(fp, "=" * 110)


def fetch(url, timeout=20):
    try:
        return session.get(url, timeout=timeout, allow_redirects=True)
    except Exception as e:
        return e


def context_hits(text, keyword, radius=450, limit=12):
    result = []
    lower = text.lower()
    needle = keyword.lower()
    pos = 0
    while len(result) < limit:
        idx = lower.find(needle, pos)
        if idx < 0:
            break
        start = max(0, idx - radius)
        end = min(len(text), idx + len(keyword) + radius)
        result.append((idx, text[start:end]))
        pos = idx + max(1, len(keyword))
    return result


def normalize(base_url, raw):
    raw = raw.strip()
    if raw.startswith(("javascript:", "data:", "mailto:", "tel:")):
        return None
    return urljoin(base_url, raw)


def score(url):
    u = url.lower()
    weights = {
        "prd": 50, "pds": 50, "menu": 40, "route": 40,
        "config": 35, "websquare": 25, ".xml": 60,
        ".w5": 60, ".js": 20, ".do": 60,
        "product": 35, "rate": 45
    }
    return sum(w for k, w in weights.items() if k in u)


def extract_resources(base_url, text):
    found = set()
    for raw in RESOURCE_RE.findall(text):
        u = normalize(base_url, raw)
        if u:
            found.add(u)
    for raw in URLISH_RE.findall(text):
        u = normalize(base_url, raw)
        if u:
            found.add(u)
    return found


def dump_hits(fp, label, text):
    divider(fp, "KEYWORD HITS : " + label)
    any_hit = False
    for keyword in KEYWORDS:
        hits = context_hits(text, keyword)
        if not hits:
            continue
        any_hit = True
        log(fp, f"\n>>> HIT [{keyword}] count={len(hits)}")
        for i, (pos, snippet) in enumerate(hits[:6], 1):
            log(fp, f"\n--- {keyword} #{i} @ {pos} ---")
            log(fp, snippet.replace("\x00", ""))
    if not any_hit:
        log(fp, "NO KEYWORD HITS")


def inspect(fp, idx, url):
    divider(fp, f"RESOURCE #{idx}")
    log(fp, "URL=" + url)
    r = fetch(url)
    if isinstance(r, Exception):
        log(fp, "ERROR=" + repr(r))
        return set()

    text = r.text
    log(fp, "FINAL=" + r.url)
    log(fp, "HTTP=" + str(r.status_code))
    log(fp, "CONTENT_TYPE=" + r.headers.get("content-type", ""))
    log(fp, "SIZE=" + str(len(r.content)))
    dump_hits(fp, f"RESOURCE #{idx}", text)
    return extract_resources(r.url, text)


def main():
    with open(OUT, "w", encoding="utf-8") as fp:
        divider(fp, "SBRateBot V5 한국투자저축은행 WebSquare Route Probe v2")
        log(fp, "ISA = PRD-PDS001-10")
        log(fp, "IRP = PRD-PDS001-11")
        log(fp, "목표 = 메뉴 ID -> 실제 WebSquare 화면/XML/JS -> 금리안내 submission/API 후보 추적")

        initial = set()

        for name, url in TARGETS.items():
            divider(fp, name + " INITIAL PAGE")
            r = fetch(url)
            if isinstance(r, Exception):
                log(fp, "ERROR=" + repr(r))
                continue

            log(fp, "URL=" + url)
            log(fp, "FINAL=" + r.url)
            log(fp, "HTTP=" + str(r.status_code))
            log(fp, "SIZE=" + str(len(r.content)))
            log(fp, "CONTENT_TYPE=" + r.headers.get("content-type", ""))
            dump_hits(fp, name + " INITIAL", r.text)
            initial.update(extract_resources(r.url, r.text))

        divider(fp, "INITIAL RESOURCE LIST")
        ranked = sorted(initial, key=lambda u: (-score(u), u))
        for i, u in enumerate(ranked, 1):
            log(fp, f"[{i:03d}] score={score(u):03d} {u}")

        visited = set()
        discovered = set()

        candidates = [
            u for u in ranked
            if not re.search(r"\.(?:png|jpg|jpeg|gif|svg|ico|woff2?|ttf|eot)(?:\?|$)", u, re.I)
        ][:40]

        divider(fp, "FIRST PASS")
        for i, u in enumerate(candidates, 1):
            if u in visited:
                continue
            visited.add(u)
            try:
                discovered.update(inspect(fp, i, u))
            except Exception as e:
                log(fp, "INSPECT ERROR=" + u + " / " + repr(e))
            time.sleep(0.05)

        second = [
            u for u in discovered
            if u not in visited and re.search(r"\.(?:xml|w5|js|do|wq)(?:\?|$)", u, re.I)
        ]
        second = sorted(second, key=lambda u: (-score(u), u))[:50]

        divider(fp, "SECOND PASS CANDIDATES")
        for i, u in enumerate(second, 1):
            log(fp, f"[{i:03d}] score={score(u):03d} {u}")

        divider(fp, "SECOND PASS")
        for i, u in enumerate(second, 1):
            if u in visited:
                continue
            visited.add(u)
            try:
                inspect(fp, i, u)
            except Exception as e:
                log(fp, "INSPECT ERROR=" + u + " / " + repr(e))
            time.sleep(0.05)

        divider(fp, "SUMMARY")
        log(fp, "INITIAL_RESOURCES=" + str(len(initial)))
        log(fp, "DISCOVERED_RESOURCES=" + str(len(discovered)))
        log(fp, "VISITED_RESOURCES=" + str(len(visited)))
        log(fp, "")
        log(fp, "확인 포인트:")
        log(fp, "1. PRD-PDS001-10 / PRD-PDS001-11 포함 XML/JS")
        log(fp, "2. w2xPath / welcome-file 실제 값")
        log(fp, "3. 상품 상세 XML의 submission/action")
        log(fp, "4. 금리안내/금리/rate 주변 .do 또는 API 경로")
        log(fp, "")
        log(fp, "DONE")

    print("\n완료:", OUT)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n중단됨")
        sys.exit(1)
