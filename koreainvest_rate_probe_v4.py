# -*- coding: utf-8 -*-
"""
koreainvest_rate_probe_v4.py

한국투자저축은행 WebSquare 메뉴/상품 경로 집중 추적기.
대상:
- PRD-PDS001-10 : ISA
- PRD-PDS001-11 : IRP/퇴직연금

실행:
    python koreainvest_rate_probe_v4.py

결과:
    koreainvest_rate_probe_v4_result.txt
"""

import re
import time
from collections import deque
from urllib.parse import urljoin, urlparse, urldefrag

import requests

BASE = "https://sb.koreainvestment.com"

START_URLS = [
    BASE + "/",
    BASE + "/websquare/config.xml",
]

TARGET_CODES = [
    "PRD-PDS001-10",
    "PRD-PDS001-11",
]

KEYWORDS = [
    "PRD-PDS001-10",
    "PRD-PDS001-11",
    "intrGridView",
    "금리안내",
    "ISA",
    "개인종합자산관리",
    "퇴직연금",
    "IRP",
    "w2xPath",
    "submission",
    ".do",
    ".xml",
]

MAX_VISITS = 350
TIMEOUT = 12
SLEEP = 0.03

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/142.0 Safari/537.36",
    "Accept": "*/*",
    "Referer": BASE + "/",
})

visited = set()
discovered = set(START_URLS)
queue = deque(START_URLS)

menu_hits = []
xml_candidates = []
api_candidates = []
interesting = []

# quoted URL/path-like strings
QUOTED_RE = re.compile(r'["\']([^"\']+)["\']')
ACTION_RE = re.compile(
    r'(?:action|url|service|endpoint|src|href|w2xPath)\s*[:=]\s*["\']([^"\']+)["\']',
    re.I,
)


def clean_url(raw, parent):
    if not raw:
        return None

    raw = raw.strip().replace("&amp;", "&")

    if raw.startswith("//"):
        raw = "https:" + raw

    # Only keep plausible resources/routes.
    low = raw.lower()
    plausible = (
        raw.startswith("/")
        or raw.startswith("http")
        or raw.startswith("./")
        or raw.startswith("../")
        or any(x in low for x in (
            ".xml", ".js", ".json", ".do", ".html", ".jsp",
            "websquare", "prd", "pds", "menu", "product"
        ))
    )
    if not plausible:
        return None

    url = urljoin(parent, raw)
    url, _ = urldefrag(url)
    p = urlparse(url)

    if p.scheme not in ("http", "https"):
        return None

    if p.netloc != urlparse(BASE).netloc:
        return None

    if any(p.path.lower().endswith(ext) for ext in (
        ".png", ".jpg", ".jpeg", ".gif", ".svg", ".woff",
        ".woff2", ".ttf", ".ico", ".mp4", ".mp3", ".pdf"
    )):
        return None

    return url


def fetch(url):
    try:
        r = session.get(url, timeout=TIMEOUT, allow_redirects=True)
        ctype = r.headers.get("content-type", "")
        text = r.text
        return r.status_code, r.url, ctype, text
    except Exception as e:
        return 0, url, "", "[ERROR] %s: %s" % (type(e).__name__, e)


def contexts(text, needle, radius=650, limit=8):
    result = []
    low = text.lower()
    target = needle.lower()
    pos = 0

    while len(result) < limit:
        idx = low.find(target, pos)
        if idx < 0:
            break
        start = max(0, idx - radius)
        end = min(len(text), idx + len(needle) + radius)
        result.append(text[start:end])
        pos = idx + len(needle)

    return result


def score_text(text):
    low = text.lower()
    weights = {
        "prd-pds001-10": 1000,
        "prd-pds001-11": 1000,
        "intrgridview": 300,
        "금리안내": 250,
        "퇴직연금": 220,
        "개인종합자산관리": 220,
        "isa": 80,
        "irp": 80,
        "w2xpath": 80,
        "submission": 60,
        ".do": 30,
        ".xml": 20,
    }

    score = 0
    for key, weight in weights.items():
        score += low.count(key) * weight
    return score


def extract_strings(text):
    vals = set()

    for m in QUOTED_RE.finditer(text):
        value = m.group(1).strip()
        if 0 < len(value) <= 500:
            low = value.lower()
            if any(x in low for x in (
                "prd", "pds", "isa", "irp", "retire",
                ".xml", ".do", "websquare", "menu",
                "service", "action", "product"
            )):
                vals.add(value)

    for m in ACTION_RE.finditer(text):
        vals.add(m.group(1).strip())

    return vals


def classify(value):
    low = value.lower()

    if ".xml" in low or "w2xpath" in low:
        return "xml"

    if ".do" in low or "/api/" in low or "service" in low or "submit" in low:
        return "api"

    return None


print("=" * 100)
print("KOREAINVEST RATE PROBE V4")
print("TARGET:", ", ".join(TARGET_CODES))
print("=" * 100)

while queue and len(visited) < MAX_VISITS:
    url = queue.popleft()

    if url in visited:
        continue

    visited.add(url)
    status, final_url, ctype, text = fetch(url)

    print("[%03d/%03d] %s %8d %s" % (
        len(visited), MAX_VISITS, status, len(text), final_url
    ))

    if status != 200 or not text:
        continue

    score = score_text(text)

    if score:
        interesting.append({
            "url": final_url,
            "size": len(text),
            "score": score,
        })

    for code in TARGET_CODES:
        if code.lower() in text.lower():
            menu_hits.append({
                "code": code,
                "url": final_url,
                "contexts": contexts(text, code),
            })
            print("    >>> MENU ROUTE HIT:", code)

    strings = extract_strings(text)

    for value in strings:
        kind = classify(value)
        if kind:
            item = {"source": final_url, "candidate": value}
            target = xml_candidates if kind == "xml" else api_candidates
            if item not in target:
                target.append(item)

        u = clean_url(value, final_url)
        if u and u not in discovered:
            discovered.add(u)

            low = u.lower()
            if any(x in low for x in (
                "prd", "pds", "menu", "product",
                "isa", "irp", "retire", "websquare"
            )):
                queue.appendleft(u)
            else:
                queue.append(u)

    time.sleep(SLEEP)


# Directly probe discovered XML/API candidates.
probe_urls = set()

for row in xml_candidates + api_candidates:
    u = clean_url(row["candidate"], row["source"])
    if u:
        probe_urls.add(u)

direct_results = []

print()
print("=" * 100)
print("XML/API CANDIDATE DIRECT PROBE")
print("=" * 100)

for i, url in enumerate(sorted(probe_urls)[:200], 1):
    status, final_url, ctype, text = fetch(url)
    score = score_text(text)

    direct_results.append({
        "url": final_url,
        "status": status,
        "ctype": ctype,
        "size": len(text),
        "score": score,
        "text": text if score >= 100 else "",
    })

    print("[%03d] HTTP=%s SIZE=%d SCORE=%d %s" % (
        i, status, len(text), score, final_url
    ))


out = []

def add(value=""):
    out.append(str(value))


add("=" * 110)
add("KOREAINVEST RATE PROBE V4 RESULT")
add("=" * 110)
add("TARGET_CODES=" + ", ".join(TARGET_CODES))
add()

add("=" * 110)
add("MENU ROUTE HIT")
add("=" * 110)

if not menu_hits:
    add("NO MENU ROUTE HIT")
else:
    for i, hit in enumerate(menu_hits, 1):
        add()
        add("[HIT %d] CODE=%s" % (i, hit["code"]))
        add("URL=" + hit["url"])
        for j, ctx in enumerate(hit["contexts"], 1):
            add()
            add("--- CONTEXT %d ---" % j)
            add(ctx)

add()
add("=" * 110)
add("XML CANDIDATES")
add("=" * 110)

if not xml_candidates:
    add("NO XML CANDIDATES")
else:
    for i, row in enumerate(xml_candidates, 1):
        add()
        add("[XML %d]" % i)
        add("SOURCE=" + row["source"])
        add("CANDIDATE=" + row["candidate"])

add()
add("=" * 110)
add("API CANDIDATES")
add("=" * 110)

if not api_candidates:
    add("NO API CANDIDATES")
else:
    for i, row in enumerate(api_candidates, 1):
        add()
        add("[API %d]" % i)
        add("SOURCE=" + row["source"])
        add("CANDIDATE=" + row["candidate"])

add()
add("=" * 110)
add("XML/API CANDIDATE DIRECT PROBE")
add("=" * 110)

ranked_direct = sorted(
    direct_results,
    key=lambda x: (x["score"], x["size"]),
    reverse=True,
)

for i, row in enumerate(ranked_direct, 1):
    add()
    add("[CANDIDATE %d] %s" % (i, row["url"]))
    add(
        "HTTP=%s SIZE=%d SCORE=%d CTYPE=%s"
        % (row["status"], row["size"], row["score"], row["ctype"])
    )

    if row["text"]:
        for kw in KEYWORDS:
            chunks = contexts(row["text"], kw, radius=500, limit=3)
            if chunks:
                add()
                add(">>> HIT [%s] count=%d" % (kw, len(chunks)))
                for chunk in chunks:
                    add(chunk)

add()
add("=" * 110)
add("TOP INTERESTING RESOURCES")
add("=" * 110)

ranked_interesting = sorted(
    interesting,
    key=lambda x: (x["score"], x["size"]),
    reverse=True,
)

for i, row in enumerate(ranked_interesting[:50], 1):
    add(
        "%02d. SCORE=%d SIZE=%d URL=%s"
        % (i, row["score"], row["size"], row["url"])
    )

add()
add("=" * 110)
add("FINAL SUMMARY")
add("=" * 110)
add("VISITED_RESOURCES=%d" % len(visited))
add("DISCOVERED_RESOURCES=%d" % len(discovered))
add("MENU_ROUTE_HITS=%d" % len(menu_hits))
add("XML_CANDIDATES=%d" % len(xml_candidates))
add("API_CANDIDATES=%d" % len(api_candidates))
add("DIRECT_PROBES=%d" % len(direct_results))
add()
add("보낼 부분:")
add("1) MENU ROUTE HIT")
add("2) XML CANDIDATES")
add("3) API CANDIDATES")
add("4) XML/API CANDIDATE DIRECT PROBE")
add("5) FINAL SUMMARY")

RESULT = "koreainvest_rate_probe_v4_result.txt"

with open(RESULT, "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print()
print("=" * 100)
print("FINAL SUMMARY")
print("=" * 100)
print("VISITED_RESOURCES =", len(visited))
print("DISCOVERED_RESOURCES =", len(discovered))
print("MENU_ROUTE_HITS =", len(menu_hits))
print("XML_CANDIDATES =", len(xml_candidates))
print("API_CANDIDATES =", len(api_candidates))
print("DIRECT_PROBES =", len(direct_results))
print("RESULT FILE =", RESULT)
print("=" * 100)
