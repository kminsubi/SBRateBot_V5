# -*- coding: utf-8 -*-
"""
SBRateBot V5 - 한국투자저축은행 Browser Network Probe v3

목표
- requests 기반 Probe v2에서 실제 화면 XML/금리 submission 경로를 찾지 못한 부분 보완
- 브라우저가 실제로 WebSquare 화면을 로딩할 때 발생하는 네트워크 요청 캡처
- ISA(PRD-PDS001-10), IRP(PRD-PDS001-11) 각각의
  XML / W5 / JS / JSON / .do / API / submission 후보 추출

필요 패키지:
    pip install selenium

실행:
    python crawler\\koreainvest_rate_probe_v3.py

출력:
    data\\koreainvest_rate_probe_v3.txt
    data\\koreainvest_rate_probe_v3.json
"""

import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

BASE = "https://sb.koreainvestment.com/"
TARGETS = {
    "ISA": "https://sb.koreainvestment.com/?PRD-PDS001-10#",
    "IRP": "https://sb.koreainvestment.com/?PRD-PDS001-11#",
}

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUT_TXT = DATA_DIR / "koreainvest_rate_probe_v3.txt"
OUT_JSON = DATA_DIR / "koreainvest_rate_probe_v3.json"

KEYWORDS = [
    "PRD-PDS001-10",
    "PRD-PDS001-11",
    "intrGridView",
    "submission",
    "submit",
    "interest",
    "intr",
    "rate",
    "금리",
    "예금",
    "ISA",
    "IRP",
    "pension",
    "retire",
]

URL_HINTS = [
    ".xml",
    ".w5",
    ".json",
    ".do",
    "/api/",
    "ajax",
    "submit",
    "submission",
    "prd",
    "pds",
    "intr",
    "rate",
    "interest",
    "websquare",
]


def score_url(url: str) -> int:
    low = url.lower()
    score = 0

    weights = {
        ".xml": 80,
        ".w5": 80,
        ".json": 70,
        ".do": 70,
        "/api/": 70,
        "submission": 60,
        "submit": 50,
        "intr": 50,
        "rate": 50,
        "interest": 50,
        "prd-pds": 60,
        "prd": 25,
        "pds": 25,
        "websquare": 15,
    }

    for k, v in weights.items():
        if k in low:
            score += v

    if any(ext in low for ext in [
        ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
        ".woff", ".woff2", ".ttf", ".css"
    ]):
        score -= 100

    return score


def interesting_url(url: str) -> bool:
    low = url.lower()
    if any(ext in low for ext in [
        ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
        ".woff", ".woff2", ".ttf"
    ]):
        return False

    return any(h in low for h in URL_HINTS)


def create_driver():
    try:
        from selenium import webdriver
        from selenium.webdriver.edge.options import Options as EdgeOptions

        options = EdgeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1600,1200")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-popup-blocking")
        options.set_capability("goog:loggingPrefs", {
            "performance": "ALL",
            "browser": "ALL",
        })

        print("[DRIVER] Microsoft Edge 시도")
        return webdriver.Edge(options=options), "Edge"

    except Exception as edge_error:
        print("[DRIVER] Edge 실패:", repr(edge_error))

    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options as ChromeOptions

        options = ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1600,1200")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-popup-blocking")
        options.set_capability("goog:loggingPrefs", {
            "performance": "ALL",
            "browser": "ALL",
        })

        print("[DRIVER] Google Chrome 시도")
        return webdriver.Chrome(options=options), "Chrome"

    except Exception as chrome_error:
        print("[DRIVER] Chrome 실패:", repr(chrome_error))
        raise RuntimeError(
            "Edge/Chrome WebDriver 실행 실패. "
            "먼저 'pip install selenium' 실행 후 다시 시도하세요."
        )


def parse_performance_logs(logs):
    rows = []

    for entry in logs:
        try:
            message = json.loads(entry["message"])["message"]
        except Exception:
            continue

        method = message.get("method", "")
        params = message.get("params", {})

        if method == "Network.responseReceived":
            response = params.get("response", {})
            request_id = params.get("requestId")

            row = {
                "type": "response",
                "requestId": request_id,
                "url": response.get("url", ""),
                "status": response.get("status"),
                "mimeType": response.get("mimeType"),
                "method": None,
                "postData": None,
            }
            rows.append(row)

        elif method == "Network.requestWillBeSent":
            request = params.get("request", {})
            row = {
                "type": "request",
                "requestId": params.get("requestId"),
                "url": request.get("url", ""),
                "status": None,
                "mimeType": None,
                "method": request.get("method"),
                "postData": request.get("postData"),
            }
            rows.append(row)

    return rows


def merge_requests(rows):
    merged = {}

    for row in rows:
        rid = row.get("requestId")
        if not rid:
            continue

        item = merged.setdefault(rid, {
            "requestId": rid,
            "url": "",
            "method": "",
            "postData": None,
            "status": None,
            "mimeType": None,
        })

        if row.get("url"):
            item["url"] = row["url"]

        if row.get("method"):
            item["method"] = row["method"]

        if row.get("postData"):
            item["postData"] = row["postData"]

        if row.get("status") is not None:
            item["status"] = row["status"]

        if row.get("mimeType"):
            item["mimeType"] = row["mimeType"]

    return list(merged.values())


def collect_dom_candidates(driver):
    result = {
        "page_title": "",
        "current_url": "",
        "page_source_hits": [],
        "scripts": [],
    }

    try:
        result["page_title"] = driver.title
    except Exception:
        pass

    try:
        result["current_url"] = driver.current_url
    except Exception:
        pass

    try:
        source = driver.page_source or ""
        for kw in KEYWORDS:
            if kw.lower() in source.lower():
                positions = [
                    m.start()
                    for m in re.finditer(re.escape(kw), source, re.I)
                ][:10]

                for pos in positions:
                    start = max(0, pos - 500)
                    end = min(len(source), pos + 900)
                    result["page_source_hits"].append({
                        "keyword": kw,
                        "position": pos,
                        "context": source[start:end],
                    })
    except Exception as e:
        result["page_source_error"] = repr(e)

    try:
        scripts = driver.execute_script("""
            return Array.from(document.scripts || []).map(function(s) {
                return s.src || "";
            }).filter(Boolean);
        """)
        result["scripts"] = scripts
    except Exception as e:
        result["scripts_error"] = repr(e)

    return result


def capture_target(driver, kind, url):
    print()
    print("=" * 100)
    print(f"[{kind}] {url}")
    print("=" * 100)

    # 이전 로그 제거
    try:
        driver.get_log("performance")
    except Exception:
        pass

    driver.get(url)

    # WebSquare 초기 렌더링 대기
    waits = [3, 5, 7]
    for sec in waits:
        time.sleep(sec)
        print(f"[WAIT] +{sec}s")

    # Edge 151 등 일부 환경에서는 driver.get_log("performance")가
    # "log type 'performance' not found" 오류를 발생시킨다.
    # Resource Timing API로 실제 로딩된 네트워크 리소스를 수집한다.
    try:
        resources = driver.execute_script("""
            return performance.getEntriesByType('resource').map(function(e) {
                return {
                    name: e.name || "",
                    initiatorType: e.initiatorType || "",
                    duration: e.duration || 0,
                    transferSize: e.transferSize || 0
                };
            });
        """) or []
    except Exception as e:
        print("[RESOURCE TIMING ERROR]", repr(e))
        resources = []

    merged = []
    for r in resources:
        merged.append({
            "requestId": None,
            "url": r.get("name", ""),
            "method": "GET/UNKNOWN",
            "postData": None,
            "status": None,
            "mimeType": r.get("initiatorType", ""),
        })

    # CDP Network 도메인이 사용 가능하면 활성화.
    # 실패해도 Resource Timing 결과로 계속 진행한다.
    try:
        driver.execute_cdp_cmd("Network.enable", {})
        print("[CDP] Network.enable OK")
    except Exception as e:
        print("[CDP] Network.enable unavailable:", repr(e))

    dom = collect_dom_candidates(driver)

    candidates = []
    for item in merged:
        url2 = item.get("url", "")
        if not url2:
            continue

        item["score"] = score_url(url2)

        if interesting_url(url2) or item["score"] > 0:
            candidates.append(item)

    # 중복 URL 제거
    unique = {}
    for item in candidates:
        key = (
            item.get("method"),
            item.get("url"),
            item.get("postData"),
        )
        if key not in unique:
            unique[key] = item

    candidates = list(unique.values())
    candidates.sort(
        key=lambda x: (
            x.get("score", 0),
            1 if x.get("method") == "POST" else 0
        ),
        reverse=True
    )

    print(f"[NETWORK] total={len(merged)} candidate={len(candidates)}")

    for idx, item in enumerate(candidates[:100], 1):
        print(
            f"[{idx:03}] "
            f"SCORE={item.get('score', 0):03} "
            f"{item.get('method') or '-':4} "
            f"HTTP={item.get('status')} "
            f"{item.get('url')}"
        )

        if item.get("postData"):
            print("      POST:", item["postData"][:500])

    return {
        "kind": kind,
        "target_url": url,
        "dom": dom,
        "network_total": len(merged),
        "candidates": candidates,
    }


def make_report(results, browser_name):
    lines = []

    def add(*args):
        lines.append(" ".join(str(x) for x in args))

    add("=" * 120)
    add("SBRateBot V5 한국투자저축은행 Browser Network Probe v3")
    add("=" * 120)
    add("BROWSER =", browser_name)
    add("ISA = PRD-PDS001-10")
    add("IRP = PRD-PDS001-11")
    add("목표 = 실제 브라우저 WebSquare 네트워크 요청에서 금리 API/submission/XML 경로 추출")
    add()

    for result in results:
        kind = result["kind"]
        dom = result["dom"]
        candidates = result["candidates"]

        add("=" * 120)
        add(kind)
        add("=" * 120)
        add("TARGET =", result["target_url"])
        add("CURRENT =", dom.get("current_url"))
        add("TITLE =", dom.get("page_title"))
        add("NETWORK_TOTAL =", result["network_total"])
        add("CANDIDATES =", len(candidates))
        add()

        add("-" * 120)
        add("NETWORK CANDIDATES")
        add("-" * 120)

        for idx, item in enumerate(candidates[:120], 1):
            add(
                f"[{idx:03}]",
                f"SCORE={item.get('score', 0):03}",
                f"METHOD={item.get('method')}",
                f"HTTP={item.get('status')}",
                f"MIME={item.get('mimeType')}",
            )
            add("URL =", item.get("url"))

            if item.get("postData"):
                add("POST =", item["postData"][:2000])

            add()

        add("-" * 120)
        add("PAGE SOURCE KEYWORD HITS")
        add("-" * 120)

        hits = dom.get("page_source_hits", [])
        if not hits:
            add("NO PAGE SOURCE KEYWORD HITS")
        else:
            for hit in hits[:60]:
                add()
                add(
                    f">>> {hit['keyword']} @ {hit['position']}"
                )
                add(hit["context"])

        add()
        add("-" * 120)
        add("SCRIPT URLS")
        add("-" * 120)

        for script in dom.get("scripts", []):
            add(script)

        add()

    add("=" * 120)
    add("다음 확인 포인트")
    add("=" * 120)
    add("1. METHOD=POST 요청")
    add("2. .do / .xml / .w5 / .json / API URL")
    add("3. POST 데이터에 PRD-PDS001-10 또는 PRD-PDS001-11 포함 여부")
    add("4. intr / rate / interest / intrGridView 관련 요청")
    add("5. ISA와 IRP에서 서로 다른 요청 URL 또는 파라미터")
    add()
    add("DONE")

    return "\n".join(lines)


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 100)
    print("SBRateBot V5 한국투자저축은행 Browser Network Probe v3")
    print("=" * 100)

    try:
        import selenium  # noqa
    except ImportError:
        print()
        print("[ERROR] selenium 패키지가 없습니다.")
        print("먼저 아래 명령 실행:")
        print()
        print("pip install selenium")
        print()
        sys.exit(1)

    driver = None

    try:
        driver, browser_name = create_driver()

        results = []
        for kind, url in TARGETS.items():
            results.append(
                capture_target(driver, kind, url)
            )

        data = {
            "browser": browser_name,
            "targets": TARGETS,
            "results": results,
        }

        OUT_JSON.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

        report = make_report(
            results,
            browser_name
        )

        OUT_TXT.write_text(
            report,
            encoding="utf-8"
        )

        print()
        print("=" * 100)
        print("완료")
        print("=" * 100)
        print("TXT :", OUT_TXT)
        print("JSON:", OUT_JSON)

    except Exception as e:
        print()
        print("[FATAL ERROR]")
        print(repr(e))
        raise

    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass


if __name__ == "__main__":
    main()
