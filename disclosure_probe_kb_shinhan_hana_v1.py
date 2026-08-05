# -*- coding: utf-8 -*-
"""
SBRateBot V5 - KB / 신한 / 하나 공시일 조사 Probe v1

목적
- 현재 운영 수집기 pension_rates_disclosure_v5_3.py의
  검증된 API/세션 함수를 그대로 재사용
- 금리 JSON은 절대 수정하지 않음
- KB / 신한 / 하나의 ISA, IRP 공식 소스에서
  날짜 후보 필드 / 날짜 포함 원문 / 날짜 키워드 주변 문맥을 조사

실행:
    cd C:\SBRateBot_V5
    py crawler\disclosure_probe_kb_shinhan_hana_v1.py

출력:
    data\disclosure_probe_kb_shinhan_hana_v1.txt
    data\disclosure_probe_kb_shinhan_hana_v1.json
"""

import json
import re
import sys
import importlib.util
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
CRAWLER_DIR = ROOT / "crawler"
DATA_DIR = ROOT / "data"

BASE_COLLECTOR = CRAWLER_DIR / "pension_rates_disclosure_v5_3.py"

OUT_TXT = DATA_DIR / "disclosure_probe_kb_shinhan_hana_v1.txt"
OUT_JSON = DATA_DIR / "disclosure_probe_kb_shinhan_hana_v1.json"

DATE_VALUE_PATTERNS = [
    re.compile(r"\b20\d{2}[-./]\d{1,2}[-./]\d{1,2}\b"),
    re.compile(r"\b20\d{6}\b"),
    re.compile(r"20\d{2}\s*년\s*\d{1,2}\s*월\s*\d{1,2}\s*일"),
]

KEY_HINTS = (
    "DATE", "DT", "YMD", "TIME", "DATETIME",
    "REG", "UPD", "CHG", "CHANGE",
    "START", "END", "APLY", "APPLY",
    "BASE", "BAS", "STD", "EFF",
    "기준", "시행", "적용", "변경", "공시",
)

TEXT_KEYWORDS = (
    "기준일", "시행일", "적용일", "변경일",
    "금리변경일", "최종금리변경일", "공시일",
    "등록일", "수정일",
)


def clean(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def load_collector():
    if not BASE_COLLECTOR.exists():
        raise FileNotFoundError(
            f"운영 수집기를 찾을 수 없습니다: {BASE_COLLECTOR}"
        )

    spec = importlib.util.spec_from_file_location(
        "pension_rates_v53",
        BASE_COLLECTOR,
    )

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    return module


def looks_like_date_value(value):
    text = clean(value)

    if not text:
        return False

    return any(
        pattern.search(text)
        for pattern in DATE_VALUE_PATTERNS
    )


def key_is_date_like(key):
    text = clean(key).upper()

    return any(
        hint in text
        for hint in KEY_HINTS
    )


def walk_date_candidates(obj, path="root"):
    """
    날짜처럼 보이는 key 또는 value를 재귀적으로 모두 수집.
    조사용이므로 자동 채택하지 않는다.
    """
    rows = []

    if isinstance(obj, dict):
        for key, value in obj.items():
            child_path = f"{path}.{key}"

            if key_is_date_like(key) or looks_like_date_value(value):
                rows.append({
                    "path": child_path,
                    "key": str(key),
                    "value": value,
                    "key_date_like": key_is_date_like(key),
                    "value_date_like": looks_like_date_value(value),
                })

            rows.extend(
                walk_date_candidates(
                    value,
                    child_path,
                )
            )

    elif isinstance(obj, list):
        for idx, value in enumerate(obj):
            rows.extend(
                walk_date_candidates(
                    value,
                    f"{path}[{idx}]",
                )
            )

    return rows


def extract_keyword_context(text, keyword, radius=220):
    text = clean(text)
    contexts = []
    start = 0

    while True:
        pos = text.find(keyword, start)

        if pos < 0:
            break

        left = max(0, pos - radius)
        right = min(
            len(text),
            pos + len(keyword) + radius,
        )

        contexts.append(
            text[left:right]
        )

        start = pos + len(keyword)

        if len(contexts) >= 10:
            break

    return contexts


def probe_kb(mod):
    results = {}

    for category, item_code in (
        ("ISA", "IB13"),
        ("IRP", "IB18"),
    ):
        print(f"[KB {category}] ITEM_CODE={item_code}")

        result, info, summary, api_url, payload_no = mod.kb_item_info(
            item_code
        )

        payload = {
            "RESULT": result,
            "RESULT_ITEM_INFO": info,
            "RESULT_ITEM_SUMMARY": summary,
        }

        candidates = walk_date_candidates(
            payload,
            f"KB.{category}",
        )

        html_contexts = []

        for section_name in (
            "이율안내",
            "상품안내",
            "유의사항",
        ):
            try:
                html = mod.kb_info_html(
                    info,
                    section_name,
                )
            except Exception:
                html = ""

            if not html:
                continue

            try:
                from bs4 import BeautifulSoup

                section_text = " ".join(
                    BeautifulSoup(
                        html,
                        "html.parser",
                    ).stripped_strings
                )
            except Exception:
                section_text = clean(html)

            for keyword in TEXT_KEYWORDS:
                for context in extract_keyword_context(
                    section_text,
                    keyword,
                ):
                    html_contexts.append({
                        "section": section_name,
                        "keyword": keyword,
                        "context": context,
                    })

        results[category] = {
            "api_url": api_url,
            "payload_no": payload_no,
            "item_name": result.get("ITEM_NAME"),
            "date_candidates": candidates,
            "keyword_contexts": html_contexts,
            "raw_blocks": payload,
        }

    return results


def probe_shinhan(mod):
    results = {}

    configs = {
        "ISA": {
            "page": "/PD_0080",
            "api": "/PD0080/selectSavPd.json",
            "pd_cd": 24014,
        },
        "IRP": {
            "page": "/PD_0081",
            "api": "/PD0081/selectSavPd.json",
            "pd_cd": 24015,
        },
    }

    for category, cfg in configs.items():
        print(f"[신한 {category}] PD_CD={cfg['pd_cd']}")

        payload, api_url = mod.shinhan_api_post(
            cfg["page"],
            cfg["api"],
            cfg["pd_cd"],
        )

        candidates = walk_date_candidates(
            payload,
            f"SHINHAN.{category}",
        )

        payload_text = json.dumps(
            payload,
            ensure_ascii=False,
        )

        contexts = []

        for keyword in TEXT_KEYWORDS:
            for context in extract_keyword_context(
                payload_text,
                keyword,
            ):
                contexts.append({
                    "keyword": keyword,
                    "context": context,
                })

        results[category] = {
            "api_url": api_url,
            "date_candidates": candidates,
            "keyword_contexts": contexts,
            "raw_payload": payload,
        }

    return results


def probe_hana(mod):
    results = {}

    configs = {
        "ISA": "https://www.hanasavings.com/YPR/YPR0103",
        "IRP": "https://www.hanasavings.com/YPR/YPR0104",
    }

    for category, url in configs.items():
        print(f"[하나 {category}] {url}")

        html, final_url = mod.fetch(
            url
        )

        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(
                html,
                "html.parser",
            )

            page_text = " ".join(
                soup.stripped_strings
            )

            # 날짜 관련 속성/스크립트 후보도 조사
            script_text = " ".join(
                clean(script.get_text(" ", strip=True))
                for script in soup.find_all("script")
            )

        except Exception:
            page_text = clean(html)
            script_text = ""

        contexts = []

        for keyword in TEXT_KEYWORDS:
            for context in extract_keyword_context(
                page_text,
                keyword,
            ):
                contexts.append({
                    "source": "page_text",
                    "keyword": keyword,
                    "context": context,
                })

            for context in extract_keyword_context(
                script_text,
                keyword,
            ):
                contexts.append({
                    "source": "script",
                    "keyword": keyword,
                    "context": context,
                })

        date_strings = []

        combined = page_text + " " + script_text

        for pattern in DATE_VALUE_PATTERNS:
            for match in pattern.finditer(
                combined
            ):
                date_strings.append({
                    "value": match.group(0),
                    "context": combined[
                        max(0, match.start() - 180):
                        min(
                            len(combined),
                            match.end() + 180,
                        )
                    ],
                })

                if len(date_strings) >= 100:
                    break

        results[category] = {
            "url": final_url,
            "keyword_contexts": contexts,
            "date_strings": date_strings,
        }

    return results


def make_txt_report(data):
    lines = []

    def add(value=""):
        lines.append(
            str(value)
        )

    add("=" * 110)
    add("SBRateBot V5 - KB / 신한 / 하나 공시일 조사 Probe v1")
    add("=" * 110)
    add(f"실행시각: {data['generated_at']}")
    add("금리 JSON 수정: NO")
    add("목적: 날짜 후보 필드/원문 조사")
    add()

    for bank in (
        "KB",
        "신한",
        "하나",
    ):
        bank_data = data.get(
            bank,
            {}
        )

        add("=" * 110)
        add(bank)
        add("=" * 110)

        for category in (
            "ISA",
            "IRP",
        ):
            item = bank_data.get(
                category,
                {}
            )

            add()
            add(f"[{bank} {category}]")
            add("-" * 110)

            if item.get("api_url"):
                add(
                    "API_URL: "
                    + str(
                        item.get("api_url")
                    )
                )

            if item.get("url"):
                add(
                    "URL: "
                    + str(
                        item.get("url")
                    )
                )

            if item.get("item_name"):
                add(
                    "ITEM_NAME: "
                    + str(
                        item.get("item_name")
                    )
                )

            candidates = item.get(
                "date_candidates",
                [],
            )

            add()
            add(
                f"DATE CANDIDATES: {len(candidates)}"
            )

            for idx, row in enumerate(
                candidates[:120],
                1,
            ):
                add(
                    f"{idx:03}. "
                    f"PATH={row.get('path')} | "
                    f"KEY={row.get('key')} | "
                    f"VALUE={row.get('value')}"
                )

            contexts = item.get(
                "keyword_contexts",
                [],
            )

            add()
            add(
                f"KEYWORD CONTEXTS: {len(contexts)}"
            )

            for idx, row in enumerate(
                contexts[:80],
                1,
            ):
                add(
                    f"{idx:03}. "
                    f"KEYWORD={row.get('keyword')} "
                    f"SOURCE={row.get('source') or row.get('section') or '-'}"
                )
                add(
                    row.get(
                        "context",
                        "",
                    )
                )
                add()

            date_strings = item.get(
                "date_strings",
                [],
            )

            if date_strings:
                add()
                add(
                    f"DATE STRINGS: {len(date_strings)}"
                )

                for idx, row in enumerate(
                    date_strings[:80],
                    1,
                ):
                    add(
                        f"{idx:03}. VALUE={row.get('value')}"
                    )
                    add(
                        row.get(
                            "context",
                            "",
                        )
                    )
                    add()

    add("=" * 110)
    add("END")
    add("=" * 110)

    return "\n".join(
        lines
    )


def main():
    print("=" * 90)
    print("KB / 신한 / 하나 공시일 조사 Probe v1")
    print("=" * 90)

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    mod = load_collector()

    output = {
        "generated_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "base_collector": str(
            BASE_COLLECTOR
        ),
        "KB": {},
        "신한": {},
        "하나": {},
        "errors": [],
    }

    try:
        output["KB"] = probe_kb(
            mod
        )
    except Exception as e:
        output["errors"].append({
            "bank": "KB",
            "error": repr(e),
        })
        print("[KB ERROR]", repr(e))

    try:
        output["신한"] = probe_shinhan(
            mod
        )
    except Exception as e:
        output["errors"].append({
            "bank": "신한",
            "error": repr(e),
        })
        print("[신한 ERROR]", repr(e))

    try:
        output["하나"] = probe_hana(
            mod
        )
    except Exception as e:
        output["errors"].append({
            "bank": "하나",
            "error": repr(e),
        })
        print("[하나 ERROR]", repr(e))

    OUT_JSON.write_text(
        json.dumps(
            output,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    OUT_TXT.write_text(
        make_txt_report(
            output
        ),
        encoding="utf-8",
    )

    print()
    print("완료")
    print("TXT :", OUT_TXT)
    print("JSON:", OUT_JSON)


if __name__ == "__main__":
    main()
