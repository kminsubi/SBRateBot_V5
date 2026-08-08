# SBRateBot V5 - Acuon JEX Endpoint Trace v4
import json, re
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE = "https://www.acuonsb.co.kr"
START_PAGE = BASE + "/sv_dpt1201170.act"
SERVICE_ID = "sd_TUB_GD_INFO_T"
OUT_JSON = Path("data/acuon_jex_endpoint_trace_v4.json")
OUT_TXT = Path("data/acuon_jex_endpoint_trace_v4.txt")

S = requests.Session()
S.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/142 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8"
})

KEYWORDS = ["createAjaxUtil", "JexAjax", "jexAjax", "execute", "JEX", "ajax",
            "service", "svc", "action", SERVICE_ID]

def fetch(url, timeout=45):
    r = S.get(url, timeout=timeout, allow_redirects=True)
    r.raise_for_status()
    if not r.encoding or r.encoding.lower() == "iso-8859-1":
        r.encoding = r.apparent_encoding or "utf-8"
    return r

def contexts(text, keyword, radius=2500, limit=20):
    out, pos = [], 0
    low, key = text.lower(), keyword.lower()
    while len(out) < limit:
        i = low.find(key, pos)
        if i < 0:
            break
        out.append(text[max(0, i-radius):min(len(text), i+len(keyword)+radius)])
        pos = i + len(keyword)
    return out

def extract_urls(text):
    out = set()
    # quoted strings
    pattern = r"[\"']([^\"'<>]{1,350})[\"']"
    for m in re.finditer(pattern, text):
        value = m.group(1).strip()
        low = value.lower()
        if any(x in low for x in (".act", ".json", ".do", ".ajax", "/api/",
                                  "ajax", "jex", "service", "interface", "gateway")):
            if value.startswith("/"):
                value = urljoin(BASE, value)
            out.add(value)
    return sorted(out)

def score_script(url, text):
    hits = {}
    for key in KEYWORDS:
        count = text.lower().count(key.lower())
        if count:
            hits[key] = count
    score = hits.get("createAjaxUtil", 0)*20 + hits.get(SERVICE_ID, 0)*20
    score += hits.get("JexAjax", 0)*10 + hits.get("jexAjax", 0)*5
    score += min(hits.get("ajax", 0), 20) + min(hits.get("execute", 0), 10)
    if "jex" in url.lower():
        score += 10
    return score, hits

def analyze_js(url):
    r = fetch(url)
    text = r.text
    score, hits = score_script(url, text)
    item = {
        "url": r.url, "size": len(r.content), "score": score, "hits": hits,
        "urls": extract_urls(text), "contexts": {}
    }
    if score > 0:
        for key in KEYWORDS:
            if key.lower() in text.lower():
                item["contexts"][key] = contexts(text, key)
    return item

def main():
    print("="*84)
    print("SBRateBot V5 Acuon JEX Endpoint Trace v4")
    print("="*84)

    page = fetch(START_PAGE)
    soup = BeautifulSoup(page.text, "html.parser")
    scripts = []
    for tag in soup.find_all("script", src=True):
        u = urljoin(page.url, tag.get("src"))
        if u not in scripts:
            scripts.append(u)

    print("[1] script count:", len(scripts))
    analyzed = []
    for i, url in enumerate(scripts, 1):
        print(f"[{i}/{len(scripts)}] {url}")
        try:
            item = analyze_js(url)
            analyzed.append(item)
            if item["score"] > 0:
                print("   score:", item["score"], "hits:", item["hits"])
        except Exception as e:
            analyzed.append({"url": url, "score": -1, "error": repr(e)})
            print("   FAIL:", e)

    # Search referenced JS URLs found inside already loaded scripts.
    discovered = []
    for item in analyzed:
        for u in item.get("urls", []):
            if (u.startswith("http") and "acuonsb.co.kr" in u and
                ".js" in u.lower() and u not in scripts and u not in discovered):
                discovered.append(u)

    print("[2] additional JS:", len(discovered))
    extra = []
    for i, url in enumerate(discovered[:30], 1):
        print(f"[{i}/{min(len(discovered),30)}] {url}")
        try:
            item = analyze_js(url)
            extra.append(item)
            if item["score"] > 0:
                print("   score:", item["score"], "hits:", item["hits"])
        except Exception as e:
            extra.append({"url": url, "score": -1, "error": repr(e)})

    all_items = analyzed + extra
    all_items.sort(key=lambda x: x.get("score", -1), reverse=True)

    definitions = []
    for item in all_items:
        ctx = item.get("contexts", {}).get("createAjaxUtil")
        if ctx:
            definitions.append({
                "url": item.get("url"),
                "score": item.get("score"),
                "contexts": ctx,
                "urls": item.get("urls", [])
            })

    result = {
        "start_page": page.url,
        "service_id": SERVICE_ID,
        "createAjaxUtil_definitions": definitions,
        "ranked_scripts": all_items
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "="*100, "SBRateBot V5 Acuon JEX Endpoint Trace v4", "="*100,
        f"START_PAGE={page.url}", f"SERVICE_ID={SERVICE_ID}",
        "", "CREATEAJAXUTIL DEFINITIONS",
        json.dumps(definitions, ensure_ascii=False, indent=2),
        "", "TOP RANKED SCRIPTS"
    ]
    for item in all_items[:20]:
        lines += [
            "-"*100,
            "URL: " + str(item.get("url")),
            "SCORE: " + str(item.get("score")),
            "HITS: " + json.dumps(item.get("hits", {}), ensure_ascii=False),
            "URLS: " + json.dumps(item.get("urls", []), ensure_ascii=False, indent=2),
            "CONTEXTS: " + json.dumps(item.get("contexts", {}), ensure_ascii=False, indent=2)
        ]
    OUT_TXT.write_text("\n".join(lines), encoding="utf-8")

    print("="*84)
    print("완료 / createAjaxUtil 정의 후보:", len(definitions))
    for d in definitions[:10]:
        print(" ->", d["url"], "score:", d["score"])
    print("JSON:", OUT_JSON)
    print("TXT :", OUT_TXT)
    print("※ 기존 ISA/IRP 금리 데이터는 수정하지 않습니다.")

if __name__ == "__main__":
    main()
