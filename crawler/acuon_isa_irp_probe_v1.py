# SBRateBot V5 - Acuon Savings ISA / IRP Probe v1
import json, re
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE = "https://www.acuonsb.co.kr"
LIST_URL = BASE + "/sv_pdt0010113.act"
OUT_JSON = Path("data/acuon_isa_irp_probe_v1.json")
OUT_TXT = Path("data/acuon_isa_irp_probe_v1.txt")

TARGETS = {
    "IRP": ["퇴직연금정기예금", "퇴직연금", "IRP", "DC/IRP"],
    "ISA": ["ISA정기예금", "ISA"],
}

S = requests.Session()
S.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/142 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
})

def fetch(url):
    r = S.get(url, timeout=30, allow_redirects=True)
    r.raise_for_status()
    if not r.encoding or r.encoding.lower() == "iso-8859-1":
        r.encoding = r.apparent_encoding or "utf-8"
    return r

def clean(text):
    return re.sub(r"\\s+", " ", str(text or "")).strip()

def contexts(text, keyword, radius=1200, limit=30):
    out, pos = [], 0
    low, key = text.lower(), keyword.lower()
    while len(out) < limit:
        i = low.find(key, pos)
        if i < 0:
            break
        out.append(text[max(0, i-radius):min(len(text), i+len(keyword)+radius)])
        pos = i + len(keyword)
    return out

def extract_endpoints(text):
    found = set()
    patterns = [
        r"""["']([^"']+\.(?:act|do|json|ajax)(?:\?[^"']*)?)["']""",
        r"""url\s*:\s*["']([^"']+)["']""",
        r"""(?:location\.href|window\.location)\s*=\s*["']([^"']+)["']""",
    ]
    for pat in patterns:
        for value in re.findall(pat, text, flags=re.I):
            if not value.startswith("javascript:"):
                found.add(urljoin(BASE, value))
    return sorted(found)

def extract_codes(text):
    found = set()
    patterns = [
        r"""(?:prod|product|goods|item|pdt)[_-]?(?:cd|code|no|id)["']?\s*[:=]\s*["']?([A-Za-z0-9_-]{2,30})""",
        r"""(?:PRD|PROD|PDT|ITEM)_[A-Z_]*(?:CD|CODE|NO|ID)["']?\s*[:=]\s*["']?([A-Za-z0-9_-]{2,30})""",
    ]
    for pat in patterns:
        found.update(re.findall(pat, text, flags=re.I))
    return sorted(found)

def target_elements(soup, keywords):
    found, seen = [], set()
    for node in soup.find_all(string=True):
        txt = clean(node)
        if not txt or not any(k.lower() in txt.lower() for k in keywords):
            continue
        el = node.parent
        candidates = [el]
        p = el
        for _ in range(6):
            if p.parent is None:
                break
            p = p.parent
            candidates.append(p)

        best = el
        for c in candidates:
            ctext = clean(c.get_text(" ", strip=True))
            if 5 <= len(ctext) <= 1500:
                best = c

        raw = str(best)
        if raw in seen:
            continue
        seen.add(raw)

        attrs = []
        for tag in best.find_all(True):
            for name, value in tag.attrs.items():
                if name.lower().startswith("data-") or name.lower() in (
                    "href", "onclick", "id", "name", "value", "action"
                ):
                    attrs.append({"tag": tag.name, "attr": name, "value": value})

        found.append({
            "text": clean(best.get_text(" ", strip=True)),
            "html": raw[:15000],
            "attrs": attrs,
            "codes": extract_codes(raw),
            "endpoints": extract_endpoints(raw),
        })
    return found

def main():
    print("="*84)
    print("SBRateBot V5 Acuon ISA / IRP Probe v1")
    print("="*84)

    r = fetch(LIST_URL)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    result = {
        "list_url": r.url,
        "http": r.status_code,
        "size": len(r.content),
        "targets": {},
        "scripts": [],
        "page_endpoints": extract_endpoints(html),
        "page_codes": extract_codes(html),
    }

    print("[1] 공식 예금상품 페이지")
    print("    HTTP:", r.status_code, "/ size:", len(r.content))

    for kind, keywords in TARGETS.items():
        elements = target_elements(soup, keywords)
        result["targets"][kind] = {
            "elements": elements,
            "contexts": {kw: contexts(html, kw) for kw in keywords if kw.lower() in html.lower()},
        }
        print(f"    {kind}: 관련 DOM 후보 {len(elements)}개")
        for x in elements[:5]:
            print("      -", x["text"][:180])
            if x["codes"]:
                print("        codes:", x["codes"])
            if x["endpoints"]:
                print("        endpoints:", x["endpoints"][:5])

    print("\n[2] JavaScript 분석")
    script_urls = []
    for tag in soup.find_all("script", src=True):
        url = urljoin(r.url, tag.get("src"))
        if "acuonsb.co.kr" in url and url not in script_urls:
            script_urls.append(url)

    print("    script count:", len(script_urls))
    for idx, url in enumerate(script_urls, 1):
        print(f"    [{idx}/{len(script_urls)}] {url}")
        try:
            sr = fetch(url)
            text = sr.text
            findings = {}
            for kind, keywords in TARGETS.items():
                hits = {kw: contexts(text, kw) for kw in keywords if kw.lower() in text.lower()}
                if hits:
                    findings[kind] = hits
            item = {
                "url": sr.url,
                "size": len(sr.content),
                "target_findings": findings,
                "endpoints": extract_endpoints(text),
                "codes": extract_codes(text),
            }
            result["scripts"].append(item)
            if findings:
                print("        >>> target hit:", list(findings))
                print("        codes:", item["codes"][:20])
                print("        endpoints:", item["endpoints"][:20])
        except Exception as e:
            result["scripts"].append({"url": url, "error": repr(e)})
            print("        FAIL:", e)

    inline = "\n".join(
        tag.get_text("\n") for tag in soup.find_all("script") if not tag.get("src")
    )
    result["inline_script"] = {
        "size": len(inline),
        "endpoints": extract_endpoints(inline),
        "codes": extract_codes(inline),
        "target_findings": {},
    }
    for kind, keywords in TARGETS.items():
        hits = {kw: contexts(inline, kw) for kw in keywords if kw.lower() in inline.lower()}
        if hits:
            result["inline_script"]["target_findings"][kind] = hits

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["="*100, "SBRateBot V5 Acuon ISA / IRP Probe v1", "="*100, ""]
    for kind in ("ISA", "IRP"):
        lines += ["="*100, kind, "="*100]
        for idx, el in enumerate(result["targets"][kind]["elements"], 1):
            lines += [
                f"\n[ELEMENT {idx}]",
                "TEXT: " + el["text"],
                "CODES: " + repr(el["codes"]),
                "ENDPOINTS: " + repr(el["endpoints"]),
                "ATTRS: " + json.dumps(el["attrs"], ensure_ascii=False),
                "HTML:",
                el["html"],
            ]

    lines += ["", "="*100, "INLINE SCRIPT", "="*100,
              json.dumps(result["inline_script"], ensure_ascii=False, indent=2)]
    lines += ["", "="*100, "EXTERNAL SCRIPTS", "="*100]
    for item in result["scripts"]:
        lines.append("\n" + item.get("url", ""))
        if item.get("error"):
            lines.append(item["error"])
        else:
            lines.append("CODES: " + repr(item.get("codes", [])))
            lines.append("ENDPOINTS: " + repr(item.get("endpoints", [])))
            if item.get("target_findings"):
                lines.append(json.dumps(item["target_findings"], ensure_ascii=False, indent=2))

    OUT_TXT.write_text("\n".join(lines), encoding="utf-8")

    print("\n"+"="*84)
    print("완료")
    print("="*84)
    print("JSON:", OUT_JSON)
    print("TXT :", OUT_TXT)
    print("※ isa_rates.json / irp_rates.json은 수정하지 않습니다.")

if __name__ == "__main__":
    main()
