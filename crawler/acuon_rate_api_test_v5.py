# ============================================================
# SBRateBot V5 - ACUON ISA / IRP JEX API Direct Test v5
# ============================================================

import json
import re
import requests

BASE_URL = "https://www.acuonsb.co.kr"
API_URL = f"{BASE_URL}/sd_TUB_GD_INFO_T.jct"

PRODUCTS = {
    "ISA": {"GD_INFO_C": "1201170"},
    "IRP": {"GD_INFO_C": "1201171"},
}

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/142 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": BASE_URL,
    "Referer": f"{BASE_URL}/",
})

RATE_KEYWORDS = [
    "rate", "rt", "interest", "intr",
    "금리", "이율", "적용금리", "기본금리", "약정금리"
]

def scan_json(obj, path="root"):
    results = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            current = f"{path}.{key}"
            if any(k.lower() in str(key).lower() for k in RATE_KEYWORDS):
                results.append((current, value))
            results.extend(scan_json(value, current))
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            results.extend(scan_json(value, f"{path}[{i}]"))
    return results

def scan_percentages(text):
    return sorted(set(re.findall(r"\b\d+(?:\.\d+)?\s*%", text)))

def scan_numeric_candidates(obj, path="root"):
    results = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            current = f"{path}.{key}"
            if isinstance(value, (int, float)) and 0 < float(value) < 20:
                results.append((current, value))
            elif isinstance(value, str):
                try:
                    number = float(value.strip())
                    if 0 < number < 20:
                        results.append((current, value))
                except ValueError:
                    pass
            results.extend(scan_numeric_candidates(value, current))
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            results.extend(scan_numeric_candidates(value, f"{path}[{i}]"))
    return results

def call_api(product_name, params):
    print("\n" + "=" * 80)
    print(product_name)
    print("=" * 80)

    payload_json = json.dumps(params, ensure_ascii=False, separators=(",", ":"))
    payload = {"_JSON_": payload_json}

    print("[REQUEST]")
    print("URL :", API_URL)
    print("JSON:", payload_json)

    try:
        response = session.post(API_URL, data=payload, timeout=20, allow_redirects=True)
    except Exception as e:
        print("[REQUEST ERROR]", e)
        return

    print("\n[RESPONSE]")
    print("STATUS :", response.status_code)
    print("URL    :", response.url)
    print("TYPE   :", response.headers.get("Content-Type"))
    print("LENGTH :", len(response.content))

    text = response.text
    print("\n[RAW RESPONSE]")
    print("-" * 80)
    print(text[:10000])
    if len(text) > 10000:
        print(f"... truncated (total {len(text):,} chars)")

    try:
        data = response.json()
    except Exception:
        print("\n[JSON PARSE] JSON 응답 아님")
        print("[PERCENTAGE CANDIDATES]", scan_percentages(text))
        return

    print("\n[JSON PARSE] SUCCESS")
    pretty = json.dumps(data, ensure_ascii=False, indent=2)
    print("\n[JSON RESPONSE]")
    print(pretty[:20000])
    if len(pretty) > 20000:
        print(f"... truncated (total {len(pretty):,} chars)")

    print("\n[RATE KEY CANDIDATES]")
    fields = scan_json(data)
    if fields:
        for path, value in fields:
            print(path, "=", value)
    else:
        print("금리 관련 key 발견 안됨")

    print("\n[NUMERIC VALUE CANDIDATES 0~20]")
    nums = scan_numeric_candidates(data)
    if nums:
        for path, value in nums:
            print(path, "=", value)
    else:
        print("후보 없음")

    print("\n[PERCENTAGE CANDIDATES]")
    values = scan_percentages(pretty)
    print(values if values else "없음")

def main():
    print("=" * 80)
    print("SBRateBot V5 ACUON ISA / IRP JEX API TEST v5")
    print("=" * 80)
    print("API:", API_URL)

    for product_name, params in PRODUCTS.items():
        call_api(product_name, params)

    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
