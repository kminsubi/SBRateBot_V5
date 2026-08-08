# SBRateBot V5 - Shinhan ISA/IRP Bundle Probe v2
# 핵심 JS 번들을 재시도/긴 timeout으로 직접 수집하고
# PD_0080(ISA), PD_0081(IRP) 주변의 API/action 후보를 추적한다.
#
# Run:
#   python crawler/shinhan_isa_irp_probe_v2.py
#
# Output:
#   data/shinhan_isa_irp_probe_v2.json
#   data/shinhan_bundle_cache/*.js

import json
import re
import ssl
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

BASE_URL = "https://www.shinhansavings.com/"

TARGETS = {
    "ISA": {
        "view_id": "PD_0080",
        "name": "ISA정기예금",
    },
    "IRP": {
        "view_id": "PD_0081",
        "name": "퇴직연금 정기예금",
    },
}

# 이전 실행에서 확인된 핵심 번들.
KNOWN_BUNDLES = [
    "https://www.shinhansavings.com/static/js/48981.11fd1c49.js",
    "https://www.shinhansavings.com/static/js/main.ceea2362.js",
]

OUTPUT = Path("data/shinhan_isa_irp_probe_v2.json")
CACHE_DIR = Path("data/shinhan_bundle_cache")

ssl._create_default_https_context = ssl._create_unverified_context


def request(url, timeout=120, range_header=None):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/142.0 Safari/537.36"
        ),
        "Accept": "*/*",
        "Accept-Encoding": "identity",
        "Referer": BASE_URL,
        "Connection": "close",
    }

    if range_header:
        headers["Range"] = range_header

    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req, timeout=timeout) as res:
        return {
            "status": getattr(res, "status", None),
            "headers": dict(res.headers.items()),
            "data": res.read(),
            "final_url": res.geturl(),
        }


def decode_bytes(raw, headers=None):
    charset = "utf-8"

    if headers:
        ctype = headers.get("Content-Type", "")
        m = re.search(r"charset=([A-Za-z0-9._-]+)", ctype, flags=re.I)
        if m:
            charset = m.group(1)

    try:
        return raw.decode(charset, errors="replace")
    except LookupError:
        return raw.decode("utf-8", errors="replace")


def fetch_with_retry(url, attempts=5):
    last_error = None

    for attempt in range(1, attempts + 1):
        timeout = 90 + (attempt * 60)

        try:
            print(
                f"      전체 다운로드 시도 {attempt}/{attempts} "
                f"(timeout={timeout}s)"
            )

            res = request(url, timeout=timeout)

            if res["data"]:
                print(
                    f"      성공: {len(res['data']):,} bytes "
                    f"(HTTP {res['status']})"
                )
                return res["data"], res["headers"], "full"

        except Exception as e:
            last_error = repr(e)
            print("      실패:", e)

        time.sleep(min(2 * attempt, 8))

    print("      전체 다운로드 실패 → Range 분할 시도")

    try:
        raw, headers = fetch_by_ranges(url)
        if raw:
            return raw, headers, "range"
    except Exception as e:
        last_error = repr(e)
        print("      Range 다운로드 실패:", e)

    raise RuntimeError(last_error or "download failed")


def fetch_by_ranges(url, chunk_size=512 * 1024, max_chunks=80):
    # 서버가 Range를 지원하면 큰 번들을 작은 조각으로 받는다.
    chunks = []
    headers = {}
    start = 0

    for index in range(max_chunks):
        end = start + chunk_size - 1
        range_header = f"bytes={start}-{end}"

        print(f"        chunk {index + 1}: {range_header}")

        res = request(
            url,
            timeout=120,
            range_header=range_header,
        )

        data = res["data"]
        headers = res["headers"]

        if not data:
            break

        status = res["status"]
        content_range = headers.get("Content-Range", "")

        # Range 미지원 서버가 200으로 전체 파일을 보내면 그대로 사용.
        if status == 200 and index == 0:
            print("        서버가 Range 대신 전체 파일 반환")
            return data, headers

        chunks.append(data)

        if status != 206:
            break

        m = re.search(r"bytes\s+(\d+)-(\d+)/(\d+|\*)", content_range)
        if m:
            actual_end = int(m.group(2))
            total = m.group(3)

            if total != "*" and actual_end + 1 >= int(total):
                break

            start = actual_end + 1
        else:
            if len(data) < chunk_size:
                break
            start += len(data)

        time.sleep(0.4)

    return b"".join(chunks), headers


def unique(values):
    out = []
    seen = set()

    for value in values:
        if value and value not in seen:
            seen.add(value)
            out.append(value)

    return out


def get_main_bundle_urls():
    urls = []

    try:
        res = request(BASE_URL, timeout=60)
        html = decode_bytes(res["data"], res["headers"])

        srcs = re.findall(
            r'<script[^>]+src=["\']([^"\']+)["\']',
            html,
            flags=re.I,
        )

        urls.extend(urljoin(BASE_URL, src) for src in srcs)

    except Exception as e:
        print("[WARN] 메인 페이지 script 탐색 실패:", e)

    # 확인된 핵심 번들은 항상 포함.
    urls.extend(KNOWN_BUNDLES)

    # 핵심 번들 우선.
    urls = unique(urls)
    urls.sort(
        key=lambda x: (
            0 if "/static/js/main." in x else
            1 if "/static/js/48981." in x else
            2
        )
    )

    return urls


def contexts(text, keyword, radius=1800, limit=40):
    result = []
    start = 0

    while len(result) < limit:
        idx = text.find(keyword, start)

        if idx < 0:
            break

        left = max(0, idx - radius)
        right = min(len(text), idx + len(keyword) + radius)

        result.append(text[left:right])
        start = idx + len(keyword)

    return result


def extract_candidates(text):
    quoted = re.findall(
        r'["\']([^"\']{2,400})["\']',
        text,
    )

    interesting = (
        "/api/",
        "api/",
        ".do",
        "axios",
        "fetch(",
        "product",
        "deposit",
        "saving",
        "rate",
        "interest",
        "intr",
        "goods",
        "prd",
        "PD_0080",
        "PD_0081",
        "ISA",
        "IRP",
        "퇴직연금",
        "정기예금",
    )

    actions = unique(
        value
        for value in quoted
        if any(k.lower() in value.lower() for k in interesting)
    )

    urls = unique(
        re.findall(r'https?://[^"\'\s<>\\]+', text, flags=re.I)
    )

    paths = unique(
        re.findall(
            r'["\']((?:/[A-Za-z0-9_.?=&%{}:$@~+,\-/]+){1,})["\']',
            text,
        )
    )

    api_paths = [
        p for p in paths
        if any(
            key in p.lower()
            for key in (
                "api",
                "product",
                "deposit",
                "rate",
                "interest",
                "prd",
                "goods",
                "pd_",
            )
        )
    ]

    return {
        "urls": urls[:300],
        "api_paths": unique(api_paths)[:500],
        "actions": actions[:700],
    }


def save_bundle(url, raw):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    name = url.split("/")[-1].split("?")[0]
    if not name.endswith(".js"):
        name += ".js"

    path = CACHE_DIR / name
    path.write_bytes(raw)
    return str(path)


def main():
    print("=" * 72)
    print("SBRateBot V5 Shinhan ISA / IRP Bundle Probe v2")
    print("PD_0080 = ISA정기예금 / PD_0081 = 퇴직연금 정기예금")
    print("=" * 72)

    bundle_urls = get_main_bundle_urls()

    # 상품 추적에 의미 있는 static JS 중심으로 제한.
    static_urls = [
        url for url in bundle_urls
        if "/static/js/" in url
    ]

    if not static_urls:
        static_urls = KNOWN_BUNDLES[:]

    print(f"\n핵심 JS 대상: {len(static_urls)}개")

    result = {
        "bank": "신한저축은행",
        "collected_at": datetime.now().isoformat(timespec="seconds"),
        "source": BASE_URL,
        "targets": TARGETS,
        "bundles": [],
        "findings": {},
    }

    loaded = []

    for i, url in enumerate(static_urls, 1):
        print(f"\n[{i}/{len(static_urls)}] {url}")

        item = {
            "url": url,
            "status": "failed",
        }

        try:
            raw, headers, method = fetch_with_retry(url)
            text = decode_bytes(raw, headers)
            cache_path = save_bundle(url, raw)

            item.update({
                "status": "ok",
                "method": method,
                "bytes": len(raw),
                "cache_path": cache_path,
            })

            loaded.append({
                "url": url,
                "text": text,
            })

        except Exception as e:
            item["error"] = repr(e)
            print("    최종 실패:", e)

        result["bundles"].append(item)

    for label, meta in TARGETS.items():
        view_id = meta["view_id"]

        print("\n" + "-" * 72)
        print(f"{label} 추적: {view_id}")
        print("-" * 72)

        finding = {
            "view_id": view_id,
            "name": meta["name"],
            "bundle_hits": [],
            "urls": [],
            "api_paths": [],
            "actions": [],
        }

        for bundle in loaded:
            text = bundle["text"]

            # view id뿐 아니라 상품명도 같이 탐색.
            keywords = [view_id, meta["name"]]

            for keyword in keywords:
                if keyword not in text:
                    continue

                ctxs = contexts(text, keyword)

                finding["bundle_hits"].append({
                    "bundle": bundle["url"],
                    "keyword": keyword,
                    "hit_count": text.count(keyword),
                    "contexts": ctxs[:20],
                })

                for ctx in ctxs:
                    candidates = extract_candidates(ctx)

                    finding["urls"].extend(candidates["urls"])
                    finding["api_paths"].extend(candidates["api_paths"])
                    finding["actions"].extend(candidates["actions"])

        finding["urls"] = unique(finding["urls"])
        finding["api_paths"] = unique(finding["api_paths"])
        finding["actions"] = unique(finding["actions"])

        result["findings"][label] = finding

        print(f"bundle hits : {len(finding['bundle_hits'])}")
        print(f"URL 후보   : {len(finding['urls'])}")
        print(f"API 후보   : {len(finding['api_paths'])}")
        print(f"Action 후보: {len(finding['actions'])}")

        for p in finding["api_paths"][:20]:
            print("  API?", p)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("\n" + "=" * 72)
    print("탐색 완료")
    print("=" * 72)
    print("결과:", OUTPUT)
    print("캐시:", CACHE_DIR)

    ok = sum(
        1 for x in result["bundles"]
        if x["status"] == "ok"
    )

    print(f"핵심 JS 성공: {ok}/{len(result['bundles'])}")

    if ok:
        print("\n결과 JSON에서 findings > ISA / IRP 를 확인하면 됩니다.")
    else:
        print("\n핵심 JS가 모두 실패했습니다. 실행 로그를 그대로 보내주세요.")


if __name__ == "__main__":
    main()
