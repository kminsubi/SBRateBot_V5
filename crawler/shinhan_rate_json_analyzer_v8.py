# ==========================================
# SBRateBot V5
# Shinhan ISA / IRP Saved JSON Analyzer v8
#
# 입력:
#   data/shinhan_rate_api_test_v7.json
#
# 목적:
# - 저장된 v7 응답을 다시 API 호출 없이 오프라인 분석
# - JSON 전체를 재귀 순회
# - TERM / APPL_RATE / 기간 / 금리 / 이율 관련 값 탐색
# - 3/6/12/24/36개월 후보를 가능한 한 많이 추출
#
# 출력:
#   data/shinhan_rate_analysis_v8.json
#   data/shinhan_rate_analysis_v8.txt
# ==========================================

import json
import re
from pathlib import Path


INPUT = Path("data/shinhan_rate_api_test_v7.json")
OUT_JSON = Path("data/shinhan_rate_analysis_v8.json")
OUT_TXT = Path("data/shinhan_rate_analysis_v8.txt")

TARGET_MONTHS = {3, 6, 12, 24, 36}

TERM_KEYS = {
    "TERM",
    "term",
    "TRM",
    "trm",
    "MONTH",
    "month",
    "MON",
    "mon",
    "PERIOD",
    "period",
    "JN_TRM",
    "jnTrm",
}

RATE_KEYWORDS = (
    "rate",
    "intr",
    "interest",
    "appl_rate",
    "applrate",
    "int_rt",
    "int_rate",
    "금리",
    "이율",
)

TYPE_KEYWORDS = (
    "db",
    "dc",
    "irp",
    "isa",
    "퇴직",
    "연금",
)


def key_is_rate(key):
    low = str(key).lower()
    return any(word in low for word in RATE_KEYWORDS)


def key_is_term(key):
    return str(key) in TERM_KEYS


def parse_number(value):
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip().replace(",", "")

    m = re.search(r"-?\d+(?:\.\d+)?", text)

    if not m:
        return None

    try:
        return float(m.group(0))
    except Exception:
        return None


def parse_month(value):
    if value is None:
        return None

    if isinstance(value, (int, float)):
        month = int(float(value))
        return month if month in TARGET_MONTHS else None

    text = str(value).strip()

    patterns = [
        r"(\d+)\s*개월",
        r"(\d+)\s*month",
        r"(\d+)\s*months",
        r"^(\d+)$",
        r"(\d+)\s*년",
    ]

    for pattern in patterns:
        m = re.search(pattern, text, flags=re.I)

        if not m:
            continue

        n = int(m.group(1))

        if "년" in pattern:
            n *= 12

        if n in TARGET_MONTHS:
            return n

    return None


def flatten(obj, path="$", out=None):
    if out is None:
        out = []

    if isinstance(obj, dict):
        for key, value in obj.items():
            next_path = f"{path}.{key}"

            out.append({
                "path": next_path,
                "key": key,
                "value": value,
                "parent": obj,
            })

            flatten(value, next_path, out)

    elif isinstance(obj, list):
        for idx, value in enumerate(obj):
            flatten(
                value,
                f"{path}[{idx}]",
                out,
            )

    return out


def collect_dict_nodes(obj, path="$", out=None):
    if out is None:
        out = []

    if isinstance(obj, dict):
        out.append({
            "path": path,
            "value": obj,
        })

        for key, value in obj.items():
            collect_dict_nodes(
                value,
                f"{path}.{key}",
                out,
            )

    elif isinstance(obj, list):
        for idx, value in enumerate(obj):
            collect_dict_nodes(
                value,
                f"{path}[{idx}]",
                out,
            )

    return out


def extract_direct_pairs(node):
    obj = node["value"]

    term_values = []
    rate_values = []

    for key, value in obj.items():
        if key_is_term(key):
            month = parse_month(value)

            if month:
                term_values.append({
                    "key": key,
                    "month": month,
                    "raw": value,
                })

        if key_is_rate(key):
            rate = parse_number(value)

            if rate is not None and 0 <= rate <= 20:
                rate_values.append({
                    "key": key,
                    "rate": rate,
                    "raw": value,
                })

    pairs = []

    for term in term_values:
        for rate in rate_values:
            pairs.append({
                "path": node["path"],
                "month": term["month"],
                "rate": rate["rate"],
                "term_key": term["key"],
                "rate_key": rate["key"],
                "object": obj,
            })

    return pairs


def extract_textual_pairs(flat_items):
    pairs = []

    for item in flat_items:
        value = item["value"]

        if not isinstance(value, str):
            continue

        text = value.strip()

        # 예: 3개월 2.60%, 12개월 기준 연 3.70%
        month_matches = list(
            re.finditer(
                r"(3|6|12|24|36)\s*개월",
                text,
            )
        )

        for mm in month_matches:
            start = max(0, mm.start() - 80)
            end = min(len(text), mm.end() + 120)
            window = text[start:end]

            rm = re.search(
                r"(\d{1,2}(?:\.\d{1,4})?)\s*%",
                window,
            )

            if rm:
                pairs.append({
                    "path": item["path"],
                    "month": int(mm.group(1)),
                    "rate": float(rm.group(1)),
                    "source": "text",
                    "text": window,
                })

    return pairs


def score_pair(pair):
    score = 0

    rate_key = str(pair.get("rate_key", "")).lower()
    path = str(pair.get("path", "")).lower()
    obj_text = json.dumps(
        pair.get("object", {}),
        ensure_ascii=False,
    ).lower()

    if "appl_rate" in rate_key:
        score += 50

    if "rate" in rate_key:
        score += 20

    if "intr" in rate_key:
        score += 20

    if "interest" in rate_key:
        score += 20

    if any(word in path for word in TYPE_KEYWORDS):
        score += 10

    if any(word in obj_text for word in TYPE_KEYWORDS):
        score += 10

    return score


def analyze_target(target_data):
    success = target_data.get("successful_attempt")

    if not success:
        return {
            "error": "successful_attempt 없음",
        }

    payload = success.get("json")

    if not isinstance(payload, dict):
        return {
            "error": "저장된 JSON payload 없음",
        }

    dict_nodes = collect_dict_nodes(payload)
    flat_items = flatten(payload)

    direct_pairs = []

    for node in dict_nodes:
        direct_pairs.extend(
            extract_direct_pairs(node)
        )

    for pair in direct_pairs:
        pair["score"] = score_pair(pair)

    direct_pairs.sort(
        key=lambda x: (
            x["month"],
            -x["score"],
            x["path"],
        )
    )

    text_pairs = extract_textual_pairs(flat_items)

    # 금리 관련 키 전체
    rate_key_hits = []

    for item in flat_items:
        if key_is_rate(item["key"]):
            rate_key_hits.append({
                "path": item["path"],
                "key": item["key"],
                "value": item["value"],
            })

    # 기간 관련 키 전체
    term_key_hits = []

    for item in flat_items:
        if key_is_term(item["key"]):
            term_key_hits.append({
                "path": item["path"],
                "key": item["key"],
                "value": item["value"],
            })

    # 월별 최상위 후보
    best = {
        "3m": None,
        "6m": None,
        "12m": None,
        "24m": None,
        "36m": None,
    }

    for month in TARGET_MONTHS:
        candidates = [
            p for p in direct_pairs
            if p["month"] == month
        ]

        if candidates:
            candidates.sort(
                key=lambda x: -x["score"]
            )

            best[f"{month}m"] = {
                "rate": candidates[0]["rate"],
                "path": candidates[0]["path"],
                "rate_key": candidates[0]["rate_key"],
                "term_key": candidates[0]["term_key"],
                "score": candidates[0]["score"],
            }

    return {
        "best_candidates": best,
        "direct_pairs": direct_pairs,
        "text_pairs": text_pairs,
        "rate_key_hits": rate_key_hits,
        "term_key_hits": term_key_hits,
    }


def make_report(result):
    lines = []

    lines.append("=" * 88)
    lines.append("SBRateBot V5 Shinhan Saved JSON Analyzer v8")
    lines.append("=" * 88)
    lines.append("")

    for label, data in result.items():
        lines.append("=" * 88)
        lines.append(label)
        lines.append("=" * 88)

        if "error" in data:
            lines.append("ERROR: " + data["error"])
            lines.append("")
            continue

        lines.append("[BEST CANDIDATES]")
        lines.append(
            json.dumps(
                data["best_candidates"],
                ensure_ascii=False,
                indent=2,
            )
        )
        lines.append("")

        lines.append(
            f"[DIRECT TERM/RATE PAIRS] {len(data['direct_pairs'])}"
        )

        for idx, item in enumerate(
            data["direct_pairs"][:120],
            start=1,
        ):
            lines.append(
                f"{idx:03d}. "
                f"{item['month']}m / "
                f"{item['rate']} / "
                f"score={item['score']} / "
                f"{item['path']} / "
                f"{item['term_key']} + {item['rate_key']}"
            )
            lines.append(
                "     "
                + json.dumps(
                    item["object"],
                    ensure_ascii=False,
                )[:1500]
            )

        lines.append("")

        lines.append(
            f"[RATE KEY HITS] {len(data['rate_key_hits'])}"
        )

        for item in data["rate_key_hits"][:200]:
            lines.append(
                f"{item['path']} = {item['value']}"
            )

        lines.append("")

        lines.append(
            f"[TERM KEY HITS] {len(data['term_key_hits'])}"
        )

        for item in data["term_key_hits"][:200]:
            lines.append(
                f"{item['path']} = {item['value']}"
            )

        lines.append("")

        lines.append(
            f"[TEXT PAIRS] {len(data['text_pairs'])}"
        )

        for item in data["text_pairs"][:100]:
            lines.append(
                f"{item['month']}m / {item['rate']} / "
                f"{item['path']} / {item['text']}"
            )

        lines.append("")

    return "\n".join(lines)


def main():
    print("=" * 72)
    print("SBRateBot V5 Shinhan Saved JSON Analyzer v8")
    print("=" * 72)

    if not INPUT.exists():
        print("입력 파일이 없습니다:")
        print(INPUT)
        print()
        print("먼저 shinhan_rate_api_test_v7.py를 실행해주세요.")
        return

    raw = json.loads(
        INPUT.read_text(
            encoding="utf-8"
        )
    )

    result = {}

    for label in ("ISA", "IRP"):
        print()
        print(f"[{label}] 전체 JSON 재귀 분석")

        data = analyze_target(
            raw.get(label, {})
        )

        result[label] = data

        if "error" in data:
            print("  ERROR:", data["error"])
            continue

        print(
            "  direct pairs:",
            len(data["direct_pairs"]),
        )
        print(
            "  rate key hits:",
            len(data["rate_key_hits"]),
        )
        print(
            "  term key hits:",
            len(data["term_key_hits"]),
        )
        print(
            "  best:",
            data["best_candidates"],
        )

    OUT_JSON.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUT_JSON.write_text(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    OUT_TXT.write_text(
        make_report(result),
        encoding="utf-8",
    )

    print()
    print("=" * 72)
    print("완료")
    print("=" * 72)
    print("JSON:", OUT_JSON)
    print("TXT :", OUT_TXT)
    print()
    print(
        "TXT 파일을 보내주면 3/6/12/24/36개월 "
        "실제 금리 위치를 바로 판별할 수 있습니다."
    )


if __name__ == "__main__":
    main()
