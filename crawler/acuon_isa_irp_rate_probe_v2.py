# SBRateBot V5 - Acuon ISA / IRP Rate Probe v2
# 상세페이지 공식 금리표 추출 테스트
# isa_rates.json / irp_rates.json은 수정하지 않습니다.

import json
import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = "https://www.acuonsb.co.kr"

TARGETS = {
    "ISA": {
        "name": "ISA정기예금",
        "url": BASE + "/sv_dpt1201170.act",
        "product_id": "1201170",
    },
    "IRP": {
        "name": "퇴직연금정기예금",
        "url": BASE + "/sv_dpt0030180.act",
        "product_id": "1201171",
    },
}

OUT_JSON = Path("data/acuon_isa_irp_rate_probe_v2.json")
OUT_TXT = Path("data/acuon_isa_irp_rate_probe_v2.txt")

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/142 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
})


def clean(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def fetch(url, timeout=40):
    r = session.get(url, timeout=timeout, allow_redirects=True)
    r.raise_for_status()
    if not r.encoding or r.encoding.lower() == "iso-8859-1":
        r.encoding = r.apparent_encoding or "utf-8"
    return r


def rate_values(text):
    out = []
    for value in re.findall(r"(?<!\d)(\d{1,2}(?:\.\d{1,3})?)\s*%", text):
        try:
            number = float(value)
            if 0 <= number <= 20:
                out.append(number)
        except ValueError:
            pass
    return out


def find_rate_tables(soup):
    out = []
    for idx, table in enumerate(soup.find_all("table"), 1):
        text = clean(table.get_text(" ", strip=True))
        score = sum(k in text for k in ("금리", "이율", "기간", "개월", "12개월", "24개월", "36개월"))
        rates = rate_values(text)
        if rates:
            score += 2
        if score >= 2:
            out.append({
                "index": idx,
                "score": score,
                "text": text,
                "rates": rates,
                "html": str(table)[:30000],
            })
    out.sort(key=lambda x: x["score"], reverse=True)
    return out


def find_period_rates(text):
    result = {"3m": None, "6m": None, "12m": None, "24m": None, "36m": None}
    patterns = {
        "3m": [r"3\s*개월"],
        "6m": [r"6\s*개월"],
        "12m": [r"12\s*개월", r"1\s*년"],
        "24m": [r"24\s*개월", r"2\s*년"],
        "36m": [r"36\s*개월", r"3\s*년"],
    }

    text = clean(text)

    for key, pats in patterns.items():
        candidates = []
        for pat in pats:
            for m in re.finditer(pat, text, flags=re.I):
                after = text[m.end():m.end() + 180]
                values = rate_values(after)
                if values:
                    candidates.append(values[0])
        if candidates:
            result[key] = candidates[0]
    return result


def contexts(text, keywords, radius=800, limit=30):
    out = []
    low = text.lower()
    for keyword in keywords:
        pos = 0
        key = keyword.lower()
        while len(out) < limit:
            idx = low.find(key, pos)
            if idx < 0:
                break
            out.append({
                "keyword": keyword,
                "context": text[max(0, idx-radius):min(len(text), idx+len(keyword)+radius)]
            })
            pos = idx + len(keyword)
    return out


def extract_endpoints(text):
    found = set()
    # 단순하고 안전하게 .act / .json 문자열만 추출
    for value in re.findall(r'[/A-Za-z0-9_.?=&%-]+\.(?:act|json)(?:\?[^"\'\s<>]*)?', text, flags=re.I):
        if value.startswith("/"):
            found.add(urljoin(BASE, value))
        elif value.startswith("http"):
            found.add(value)
    return sorted(found)


def analyze(kind, cfg):
    print("\n" + "=" * 80)
    print(kind, "-", cfg["name"])
    print("=" * 80)

    r = fetch(cfg["url"])
    soup = BeautifulSoup(r.text, "html.parser")
    page_text = clean(soup.get_text(" ", strip=True))

    tables = find_rate_tables(soup)
    detected = find_period_rates(page_text)

    print("URL :", r.url)
    print("HTTP:", r.status_code)
    print("SIZE:", len(r.content))
    print("금리표 후보:", len(tables))
    print("1차 기간별 탐지:", detected)

    if tables:
        print("\n[최상위 금리표 후보]")
        print(tables[0]["text"][:1500])

    id_hits = []
    for tag in soup.find_all(id=cfg["product_id"]):
        id_hits.append({
            "tag": tag.name,
            "text": clean(tag.get_text(" ", strip=True)),
            "html": str(tag)[:10000],
        })

    inline = "\n".join(
        x.get_text("\n") for x in soup.find_all("script") if not x.get("src")
    )

    script_urls = []
    for tag in soup.find_all("script", src=True):
        u = urljoin(r.url, tag.get("src"))
        if u not in script_urls:
            script_urls.append(u)

    script_findings = []
    keys = [cfg["product_id"], cfg["name"], "금리", "이율", "rate", "interest"]

    print("외부 script:", len(script_urls))

    for idx, url in enumerate(script_urls, 1):
        try:
            sr = fetch(url, 30)
            text = sr.text
            if cfg["product_id"] in text or cfg["name"] in text:
                print(f"  TARGET HIT [{idx}] {url}")
                script_findings.append({
                    "url": sr.url,
                    "size": len(sr.content),
                    "contexts": contexts(text, keys),
                    "endpoints": extract_endpoints(text),
                })
        except Exception as e:
            script_findings.append({"url": url, "error": repr(e)})

    return {
        "kind": kind,
        "name": cfg["name"],
        "url": r.url,
        "product_id": cfg["product_id"],
        "http": r.status_code,
        "size": len(r.content),
        "detected_rates": detected,
        "page_rate_values": rate_values(page_text),
        "rate_tables": tables,
        "product_id_hits": id_hits,
        "page_contexts": contexts(
            r.text, [cfg["product_id"], cfg["name"], "금리", "이율", "개월"], radius=1000
        ),
        "page_endpoints": extract_endpoints(r.text),
        "inline_script": {
            "size": len(inline),
            "contexts": contexts(inline, keys),
            "endpoints": extract_endpoints(inline),
        },
        "external_script_findings": script_findings,
    }


def main():
    print("=" * 80)
    print("SBRateBot V5 Acuon ISA / IRP Rate Probe v2")
    print("=" * 80)

    result = {}

    for kind, cfg in TARGETS.items():
        try:
            result[kind] = analyze(kind, cfg)
        except Exception as e:
            print(kind, "FAIL:", e)
            result[kind] = {
                "kind": kind,
                "name": cfg["name"],
                "url": cfg["url"],
                "product_id": cfg["product_id"],
                "error": repr(e),
            }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "=" * 100,
        "SBRateBot V5 Acuon ISA / IRP Rate Probe v2",
        "=" * 100,
    ]

    for kind in ("ISA", "IRP"):
        d = result.get(kind, {})
        lines += [
            "",
            "=" * 100,
            kind,
            "=" * 100,
            "NAME: " + str(d.get("name")),
            "URL: " + str(d.get("url")),
            "PRODUCT_ID: " + str(d.get("product_id")),
            "HTTP: " + str(d.get("http")),
            "ERROR: " + str(d.get("error")),
            "",
            "DETECTED_RATES:",
            json.dumps(d.get("detected_rates"), ensure_ascii=False, indent=2),
            "",
            "PAGE_RATE_VALUES:",
            repr(d.get("page_rate_values")),
            "",
            "PRODUCT_ID_HITS:",
            json.dumps(d.get("product_id_hits"), ensure_ascii=False, indent=2),
            "",
            "RATE_TABLES:",
        ]

        for table in d.get("rate_tables", []):
            lines += [
                "-" * 100,
                f"TABLE #{table['index']} / SCORE={table['score']}",
                "RATES: " + repr(table["rates"]),
                "TEXT:",
                table["text"],
                "HTML:",
                table["html"],
            ]

        lines += [
            "",
            "PAGE_CONTEXTS:",
            json.dumps(d.get("page_contexts"), ensure_ascii=False, indent=2),
            "",
            "PAGE_ENDPOINTS:",
            json.dumps(d.get("page_endpoints"), ensure_ascii=False, indent=2),
            "",
            "INLINE_SCRIPT:",
            json.dumps(d.get("inline_script"), ensure_ascii=False, indent=2),
            "",
            "EXTERNAL_SCRIPT_FINDINGS:",
            json.dumps(d.get("external_script_findings"), ensure_ascii=False, indent=2),
        ]

    OUT_TXT.write_text("\n".join(lines), encoding="utf-8")

    print("\n" + "=" * 80)
    print("완료")
    print("=" * 80)
    for kind in ("ISA", "IRP"):
        print(kind, "->", result.get(kind, {}).get("detected_rates"))
    print("JSON:", OUT_JSON)
    print("TXT :", OUT_TXT)
    print("※ isa_rates.json / irp_rates.json은 수정하지 않습니다.")


if __name__ == "__main__":
    main()
