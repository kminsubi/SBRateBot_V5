# SBRateBot V5 - SBI Savings ISA / IRP Product Probe v1
import json, re
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE = "https://www.sbisb.co.kr"
LIST_URL = BASE + "/gds0010100.act"
OUT_JSON = Path("data/sbi_isa_irp_probe_v1.json")
OUT_TXT = Path("data/sbi_isa_irp_probe_v1.txt")

S = requests.Session()
S.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/142 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
})

KEYWORDS = ["ISA", "퇴직연금", "IRP", "DC형", "DC/IRP"]

def fetch(url, **kwargs):
    r = S.get(url, timeout=30, allow_redirects=True, **kwargs)
    r.raise_for_status()
    r.encoding = r.apparent_encoding or "utf-8"
    return r

def contexts(text, keyword, radius=700):
    out = []
    pos = 0
    low = text.lower()
    key = keyword.lower()
    while len(out) < 30:
        i = low.find(key, pos)
        if i < 0:
            break
        out.append(text[max(0, i-radius):min(len(text), i+len(keyword)+radius)])
        pos = i + len(keyword)
    return out

def extract_prod_codes(text):
    found = set()
    patterns = [
        r'PROD_CD["\']?\s*[:=]\s*["\']?([A-Za-z0-9_-]+)',
        r'[?&]PROD_CD=([A-Za-z0-9_-]+)',
        r'prod_cd["\']?\s*[:=]\s*["\']?([A-Za-z0-9_-]+)',
        r'[?&]prod_cd=([A-Za-z0-9_-]+)',
    ]
    for pat in patterns:
        found.update(re.findall(pat, text, flags=re.I))
    return sorted(found)

def extract_act_endpoints(text):
    eps = set()
    for x in re.findall(r'["\']([^"\']+\.act(?:\?[^"\']*)?)["\']', text, flags=re.I):
        eps.add(urljoin(BASE, x))
    return sorted(eps)

def main():
    print("="*84)
    print("SBRateBot V5 SBI ISA / IRP Product Probe v1")
    print("="*84)

    r = fetch(LIST_URL)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    result = {
        "list_url": r.url,
        "status": r.status_code,
        "prod_codes": extract_prod_codes(html),
        "keyword_contexts": {},
        "scripts": [],
        "endpoints": extract_act_endpoints(html),
        "detail_tests": [],
    }

    print("[1] 상품목록")
    print("    HTTP:", r.status_code, "/ size:", len(r.content))
    print("    PROD_CD candidates:", len(result["prod_codes"]))

    for kw in KEYWORDS:
        vals = contexts(html, kw)
        if vals:
            result["keyword_contexts"][kw] = vals
            print(f"    {kw}: {len(vals)} hit")

    print("\n[2] JS 파일 분석")
    for tag in soup.find_all("script", src=True):
        src = urljoin(r.url, tag.get("src"))
        if "sbisb.co.kr" not in src:
            continue
        try:
            sr = fetch(src)
            text = sr.text
            item = {
                "url": sr.url,
                "size": len(sr.content),
                "prod_codes": extract_prod_codes(text),
                "endpoints": extract_act_endpoints(text),
                "keyword_contexts": {},
            }
            for kw in KEYWORDS:
                vals = contexts(text, kw)
                if vals:
                    item["keyword_contexts"][kw] = vals
            result["scripts"].append(item)
            if item["prod_codes"] or item["keyword_contexts"]:
                print("   ", sr.url)
                print("      PROD_CD:", item["prod_codes"][:20])
                print("      keyword:", list(item["keyword_contexts"]))
        except Exception as e:
            result["scripts"].append({"url": src, "error": repr(e)})

    all_codes = set(result["prod_codes"])
    for item in result["scripts"]:
        all_codes.update(item.get("prod_codes", []))

    print("\n[3] 발견된 PROD_CD 상세화면 확인")
    for code in sorted(all_codes):
        for page in ("gds0010200.act", "gds0010201.act"):
            url = f"{BASE}/{page}?PROD_CD={code}"
            try:
                dr = fetch(url)
                text = BeautifulSoup(dr.text, "html.parser").get_text(" ", strip=True)
                hit = [kw for kw in KEYWORDS if kw.lower() in text.lower()]
                title = BeautifulSoup(dr.text, "html.parser").title
                title = title.get_text(" ", strip=True) if title else ""
                row = {
                    "prod_cd": code,
                    "url": dr.url,
                    "http": dr.status_code,
                    "title": title,
                    "keywords": hit,
                    "text_head": text[:2500],
                }
                result["detail_tests"].append(row)
                if hit:
                    print(f"    >>> {code} {page}: {hit}")
            except Exception as e:
                result["detail_tests"].append({
                    "prod_cd": code, "url": url, "error": repr(e)
                })

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "="*100,
        "SBI ISA / IRP PRODUCT PROBE v1",
        "="*100,
        "",
        f"LIST: {result['list_url']}",
        "",
        "PROD_CD CANDIDATES:",
        *sorted(all_codes),
        "",
        "="*100,
        "KEYWORD CONTEXTS",
        "="*100,
    ]
    for kw, vals in result["keyword_contexts"].items():
        lines.append(f"\n[{kw}]")
        lines.extend(x.replace("\r"," ").replace("\n"," ") for x in vals)

    lines += ["", "="*100, "SCRIPT FINDINGS", "="*100]
    for item in result["scripts"]:
        lines.append("\n"+item.get("url",""))
        if item.get("error"):
            lines.append(item["error"])
            continue
        lines.append("PROD_CD: "+repr(item.get("prod_codes")))
        lines.append("ENDPOINTS:")
        lines.extend(item.get("endpoints", []))
        for kw, vals in item.get("keyword_contexts", {}).items():
            lines.append(f"[{kw}]")
            lines.extend(x.replace("\r"," ").replace("\n"," ") for x in vals[:10])

    lines += ["", "="*100, "DETAIL TESTS", "="*100]
    for x in result["detail_tests"]:
        lines.append(json.dumps(x, ensure_ascii=False))

    OUT_TXT.write_text("\n".join(lines), encoding="utf-8")

    print("\n"+"="*84)
    print("완료")
    print("="*84)
    print("JSON:", OUT_JSON)
    print("TXT :", OUT_TXT)
    print("※ isa_rates.json / irp_rates.json은 수정하지 않습니다.")

if __name__ == "__main__":
    main()
