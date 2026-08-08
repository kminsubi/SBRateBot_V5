# ==========================================
# SBRateBot V5
# Shinhan ISA / IRP Chunk Probe v5
#
# PD_0080 -> aN -> Bf -> chunk/module 53147
# PD_0081 -> iN -> Rf -> chunk/module 75958
# ==========================================

from pathlib import Path
import json
import re
import ssl
import time
import urllib.request
from urllib.parse import urljoin

BASE_URL = "https://www.shinhansavings.com"
MAIN_JS_URL = BASE_URL + "/static/js/main.ceea2362.js"

TARGETS = {
    "ISA": {
        "product_code": "PD_0080",
        "chunk_id": "53147",
    },
    "IRP": {
        "product_code": "PD_0081",
        "chunk_id": "75958",
    },
}

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
CACHE_DIR = DATA_DIR / "shinhan_chunk_cache"
MAIN_CACHE = DATA_DIR / "shinhan_bundle_cache" / "main.ceea2362.js"

OUTPUT_JSON = DATA_DIR / "shinhan_chunk_probe_v5.json"
OUTPUT_TXT = DATA_DIR / "shinhan_chunk_probe_v5.txt"

DATA_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/142.0 Safari/537.36"
    ),
    "Accept": "*/*",
    "Referer": BASE_URL + "/",
}


def download(url, timeout=180, retries=4):
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            print(f"      다운로드 {attempt}/{retries}: {url}")

            req = urllib.request.Request(url, headers=HEADERS)

            with urllib.request.urlopen(
                req,
                timeout=timeout,
                context=SSL_CONTEXT,
            ) as response:
                data = response.read()

            print(f"      성공: {len(data):,} bytes")
            return data

        except Exception as exc:
            last_error = exc
            print(f"      실패: {exc}")
            time.sleep(min(attempt * 2, 8))

    raise RuntimeError(last_error)


def load_main_js():
    if MAIN_CACHE.exists():
        data = MAIN_CACHE.read_bytes()
        print(f"[1] main.js 캐시 사용: {MAIN_CACHE}")
        print(f"    {len(data):,} bytes")
        return data.decode("utf-8", errors="ignore")

    print("[1] main.js 다운로드")
    data = download(MAIN_JS_URL)
    MAIN_CACHE.parent.mkdir(parents=True, exist_ok=True)
    MAIN_CACHE.write_bytes(data)
    return data.decode("utf-8", errors="ignore")


def extract_runtime_rules(main_js):
    """
    Webpack runtime에서 chunk filename 생성 규칙 주변을 수집한다.
    보통:
      t.u = n => "static/js/" + n + "." + HASH[n] + ".js"
    같은 구조가 존재한다.
    """
    contexts = []

    patterns = [
        r'\.u\s*=\s*[A-Za-z_$][\w$]*\s*=>',
        r'\.u\s*=\s*function\s*\(',
        r'static/js/',
        r'\.js"\}',
        r'\.js"',
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, main_js):
            start = max(0, match.start() - 1500)
            end = min(len(main_js), match.end() + 5000)
            context = main_js[start:end]

            if context not in contexts:
                contexts.append(context)

            if len(contexts) >= 12:
                break

    return contexts


def find_chunk_hash(main_js, chunk_id):
    """
    main bundle 안에서 chunk ID에 대응하는 해시 후보를 찾는다.
    """
    hashes = []

    patterns = [
        rf'{re.escape(chunk_id)}:"([0-9a-f]{{6,32}})"',
        rf'{re.escape(chunk_id)}:\s*"([0-9a-f]{{6,32}})"',
        rf'"{re.escape(chunk_id)}":"([0-9a-f]{{6,32}})"',
        rf'"{re.escape(chunk_id)}":\s*"([0-9a-f]{{6,32}})"',
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, main_js, flags=re.I):
            value = match.group(1)
            if value not in hashes:
                hashes.append(value)

    return hashes


def find_literal_chunk_urls(main_js, chunk_id):
    urls = []

    # main.js 안에 실제 파일명이 문자열로 들어있는 경우
    patterns = [
        rf'[^"\'\s]{{0,120}}{re.escape(chunk_id)}[^"\'\s]{{0,120}}\.js',
        rf'static/js/[^"\'\s]*{re.escape(chunk_id)}[^"\'\s]*\.js',
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, main_js, flags=re.I):
            text = match.group(0)

            idx = text.find("static/js/")
            if idx >= 0:
                text = text[idx:]

            if text.startswith("/"):
                url = urljoin(BASE_URL, text)
            elif text.startswith("static/"):
                url = urljoin(BASE_URL + "/", text)
            else:
                continue

            if url not in urls:
                urls.append(url)

    return urls


def build_chunk_candidates(main_js, chunk_id):
    candidates = []

    for url in find_literal_chunk_urls(main_js, chunk_id):
        if url not in candidates:
            candidates.append(url)

    hashes = find_chunk_hash(main_js, chunk_id)

    # CRA/Webpack에서 흔한 형태
    for h in hashes:
        for filename in (
            f"/static/js/{chunk_id}.{h}.chunk.js",
            f"/static/js/{chunk_id}.{h}.js",
        ):
            url = BASE_URL + filename
            if url not in candidates:
                candidates.append(url)

    # 해시를 못 찾았을 때도 진단용 후보 생성
    for filename in (
        f"/static/js/{chunk_id}.chunk.js",
        f"/static/js/{chunk_id}.js",
    ):
        url = BASE_URL + filename
        if url not in candidates:
            candidates.append(url)

    return candidates, hashes


def download_target_chunk(main_js, label, chunk_id):
    candidates, hashes = build_chunk_candidates(main_js, chunk_id)

    print()
    print(f"[2] {label} chunk 탐색: {chunk_id}")
    print(f"    hash 후보: {hashes if hashes else '없음'}")
    print(f"    URL 후보 : {len(candidates)}")

    errors = []

    for idx, url in enumerate(candidates, 1):
        print(f"    후보 {idx}/{len(candidates)}")

        try:
            data = download(url, timeout=180, retries=2)

            # HTML 오류 페이지 방지
            head = data[:300].lower()
            if b"<html" in head or b"<!doctype html" in head:
                errors.append({
                    "url": url,
                    "error": "HTML response",
                })
                print("      HTML 응답 → 제외")
                continue

            cache_path = CACHE_DIR / f"{label.lower()}_{chunk_id}.js"
            cache_path.write_bytes(data)

            print(f"    저장: {cache_path}")

            return {
                "success": True,
                "url": url,
                "path": str(cache_path),
                "bytes": len(data),
                "hash_candidates": hashes,
                "candidate_urls": candidates,
                "errors": errors,
                "text": data.decode("utf-8", errors="ignore"),
            }

        except Exception as exc:
            errors.append({
                "url": url,
                "error": str(exc),
            })

    return {
        "success": False,
        "url": None,
        "path": None,
        "bytes": 0,
        "hash_candidates": hashes,
        "candidate_urls": candidates,
        "errors": errors,
        "text": "",
    }


def unique(items):
    result = []
    seen = set()

    for item in items:
        key = json.dumps(item, ensure_ascii=False, sort_keys=True) \
            if isinstance(item, dict) else str(item)

        if key not in seen:
            seen.add(key)
            result.append(item)

    return result


def analyze_chunk(text, product_code):
    result = {
        "api_urls": [],
        "path_candidates": [],
        "http_calls": [],
        "actions": [],
        "rate_keys": [],
        "period_keys": [],
        "product_code_contexts": [],
        "keyword_contexts": [],
    }

    # URL
    result["api_urls"] = unique(re.findall(
        r'https?://[^"\'`\s\\]+',
        text,
        flags=re.I,
    ))

    # API/endpoint처럼 보이는 문자열
    path_patterns = [
        r'["\'`](/api/[^"\'`]{1,180})["\'`]',
        r'["\'`](/v\d+/[^"\'`]{1,180})["\'`]',
        r'["\'`](/[A-Za-z0-9_-]+/[A-Za-z0-9_/?=&.%:-]{2,180})["\'`]',
    ]

    paths = []
    for pattern in path_patterns:
        paths.extend(re.findall(pattern, text, flags=re.I))

    result["path_candidates"] = unique(paths)[:300]

    # axios/fetch 호출 주변
    call_patterns = [
        r'fetch\([^)]{0,500}\)',
        r'\.(?:get|post|put|patch)\([^)]{0,700}\)',
        r'axios[^;]{0,900}',
    ]

    calls = []
    for pattern in call_patterns:
        calls.extend(re.findall(pattern, text, flags=re.I))

    result["http_calls"] = unique(calls)[:150]

    # action / service / endpoint 이름 후보
    action_patterns = [
        r'["\']([A-Za-z0-9_]*(?:rate|intr|interest|deposit|product|prd|goods)[A-Za-z0-9_]*)["\']',
        r'["\']([A-Za-z0-9_]*(?:select|search|detail|list|inq|inquiry)[A-Za-z0-9_]*)["\']',
    ]

    actions = []
    for pattern in action_patterns:
        actions.extend(re.findall(pattern, text, flags=re.I))

    result["actions"] = unique(actions)[:200]

    # 금리 관련 key
    result["rate_keys"] = unique(re.findall(
        r'["\']([A-Za-z0-9_]*(?:rate|intr|interest|이율|금리)[A-Za-z0-9_]*)["\']',
        text,
        flags=re.I,
    ))[:200]

    # 기간 관련 key
    result["period_keys"] = unique(re.findall(
        r'["\']([A-Za-z0-9_]*(?:month|mon|term|period|기간|개월)[A-Za-z0-9_]*)["\']',
        text,
        flags=re.I,
    ))[:200]

    # 상품 코드 주변
    for match in re.finditer(re.escape(product_code), text, flags=re.I):
        start = max(0, match.start() - 1800)
        end = min(len(text), match.end() + 3500)

        result["product_code_contexts"].append(
            text[start:end]
        )

    result["product_code_contexts"] = unique(
        result["product_code_contexts"]
    )[:20]

    # 핵심 키워드 주변
    keywords = [
        "금리",
        "이율",
        "interest",
        "rate",
        "deposit",
        "퇴직연금",
        "ISA",
        "개월",
        "month",
    ]

    contexts = []

    for keyword in keywords:
        for match in re.finditer(re.escape(keyword), text, flags=re.I):
            start = max(0, match.start() - 900)
            end = min(len(text), match.end() + 1600)
            contexts.append({
                "keyword": keyword,
                "context": text[start:end],
            })

            if len(contexts) >= 80:
                break

        if len(contexts) >= 80:
            break

    result["keyword_contexts"] = unique(contexts)

    return result


def make_text_report(payload):
    lines = []

    lines.append("=" * 88)
    lines.append("SBRateBot V5 Shinhan Chunk Probe v5")
    lines.append("=" * 88)
    lines.append("")

    runtime_contexts = payload.get("runtime_contexts", [])
    lines.append(f"WEBPACK RUNTIME CONTEXTS: {len(runtime_contexts)}")
    lines.append("")

    for label, item in payload["targets"].items():
        lines.append("=" * 88)
        lines.append(
            f"{label} / {item['product_code']} / CHUNK {item['chunk_id']}"
        )
        lines.append("=" * 88)

        download_info = item["download"]

        lines.append(f"SUCCESS: {download_info['success']}")
        lines.append(f"URL: {download_info['url']}")
        lines.append(f"BYTES: {download_info['bytes']}")
        lines.append(
            f"HASH CANDIDATES: {download_info['hash_candidates']}"
        )
        lines.append("")

        analysis = item["analysis"]

        for key in (
            "api_urls",
            "path_candidates",
            "http_calls",
            "actions",
            "rate_keys",
            "period_keys",
        ):
            values = analysis.get(key, [])

            lines.append(f"[{key.upper()}] {len(values)}")
            lines.append("-" * 88)

            for value in values:
                lines.append(str(value))

            lines.append("")

        contexts = analysis.get("product_code_contexts", [])

        lines.append(
            f"[PRODUCT CODE CONTEXTS] {len(contexts)}"
        )
        lines.append("-" * 88)

        for idx, context in enumerate(contexts, 1):
            lines.append(f"# {idx}")
            lines.append(context)
            lines.append("")

        keyword_contexts = analysis.get("keyword_contexts", [])

        lines.append(
            f"[KEYWORD CONTEXTS] {len(keyword_contexts)}"
        )
        lines.append("-" * 88)

        for idx, context in enumerate(keyword_contexts, 1):
            lines.append(
                f"# {idx} KEYWORD={context['keyword']}"
            )
            lines.append(context["context"])
            lines.append("")

    return "\n".join(lines)


def main():
    print("=" * 72)
    print("SBRateBot V5 Shinhan ISA / IRP Chunk Probe v5")
    print("ISA: PD_0080 -> chunk 53147")
    print("IRP: PD_0081 -> chunk 75958")
    print("=" * 72)

    main_js = load_main_js()

    runtime_contexts = extract_runtime_rules(main_js)

    payload = {
        "main_js": str(MAIN_CACHE),
        "runtime_contexts": runtime_contexts,
        "targets": {},
    }

    for label, cfg in TARGETS.items():
        download_info = download_target_chunk(
            main_js,
            label,
            cfg["chunk_id"],
        )

        text = download_info.pop("text")

        if text:
            analysis = analyze_chunk(
                text,
                cfg["product_code"],
            )
        else:
            analysis = {
                "api_urls": [],
                "path_candidates": [],
                "http_calls": [],
                "actions": [],
                "rate_keys": [],
                "period_keys": [],
                "product_code_contexts": [],
                "keyword_contexts": [],
            }

        payload["targets"][label] = {
            "product_code": cfg["product_code"],
            "chunk_id": cfg["chunk_id"],
            "download": download_info,
            "analysis": analysis,
        }

    OUTPUT_JSON.write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    OUTPUT_TXT.write_text(
        make_text_report(payload),
        encoding="utf-8",
    )

    print()
    print("=" * 72)
    print("탐색 완료")
    print("=" * 72)

    for label, item in payload["targets"].items():
        download_info = item["download"]
        analysis = item["analysis"]

        print()
        print(
            f"{label}: chunk {item['chunk_id']} "
            f"{'다운로드 성공' if download_info['success'] else '다운로드 실패'}"
        )

        if download_info["success"]:
            print(f"  URL       : {download_info['url']}")
            print(f"  API URL   : {len(analysis['api_urls'])}")
            print(f"  PATH 후보 : {len(analysis['path_candidates'])}")
            print(f"  HTTP 호출 : {len(analysis['http_calls'])}")
            print(f"  ACTION    : {len(analysis['actions'])}")
            print(f"  RATE KEY  : {len(analysis['rate_keys'])}")
            print(f"  PERIOD KEY: {len(analysis['period_keys'])}")

    print()
    print(f"JSON: {OUTPUT_JSON}")
    print(f"TXT : {OUTPUT_TXT}")
    print()
    print("실행 후 shinhan_chunk_probe_v5.txt를 보내주세요.")


if __name__ == "__main__":
    main()
