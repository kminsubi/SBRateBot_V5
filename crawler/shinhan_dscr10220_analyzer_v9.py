# ==========================================
# SBRateBot V5
# Shinhan dscr10220 Structure Analyzer v9
#
# 입력:
#   data/shinhan_rate_api_test_v7.json
#
# 목적:
# - ISA / IRP의 dscr10220.LIST 각 행 전체 필드 출력
# - 행별 기간/금리/구분코드 후보 비교
# - selectSavPd, dscr10230과 함께 비교
# - 실제 3/6/12/24/36개월 매핑 근거 확보
#
# 데이터 파일은 수정하지 않는 분석 전용 버전
# ==========================================

import json
from pathlib import Path


INPUT = Path("data/shinhan_rate_api_test_v7.json")
OUT_JSON = Path("data/shinhan_dscr10220_analysis_v9.json")
OUT_TXT = Path("data/shinhan_dscr10220_analysis_v9.txt")


def unwrap(row):
    if isinstance(row, dict) and isinstance(row.get("map"), dict):
        return row["map"]
    return row if isinstance(row, dict) else {}


def get_payload(target):
    attempt = target.get("successful_attempt") or {}
    payload = attempt.get("json") or {}
    return payload.get("data", payload) if isinstance(payload, dict) else {}


def get_list(data, key):
    value = data.get(key)

    if isinstance(value, dict):
        rows = value.get("LIST")
        if isinstance(rows, list):
            return rows

    if isinstance(value, list):
        return value

    return []


def interesting_fields(row):
    result = {}

    words = (
        "term", "trm", "month", "mon", "period",
        "rate", "intr", "int_", "aply", "appl",
        "class", "cd", "seq", "type", "kind",
        "name", "nm", "div", "gb", "gubun",
    )

    for key, value in row.items():
        low = str(key).lower()

        if any(word in low for word in words):
            result[key] = value

    return result


def analyze(label, target):
    data = get_payload(target)

    rows10220 = [
        unwrap(x)
        for x in get_list(data, "dscr10220")
    ]

    rows10230 = [
        unwrap(x)
        for x in get_list(data, "dscr10230")
    ]

    select_sav = data.get("selectSavPd", [])

    if not isinstance(select_sav, list):
        select_sav = []

    select_sav = [unwrap(x) for x in select_sav]

    result = {
        "dscr10220_count": len(rows10220),
        "dscr10220": [],
        "dscr10230": rows10230,
        "selectSavPd": select_sav,
    }

    for idx, row in enumerate(rows10220):
        result["dscr10220"].append({
            "index": idx,
            "interesting_fields": interesting_fields(row),
            "all_fields": row,
        })

    return result


def build_report(results):
    lines = []

    lines.append("=" * 100)
    lines.append("SBRateBot V5 Shinhan dscr10220 Structure Analyzer v9")
    lines.append("=" * 100)

    for label, result in results.items():
        lines.append("")
        lines.append("=" * 100)
        lines.append(label)
        lines.append("=" * 100)

        lines.append("")
        lines.append(
            f"[dscr10220.LIST] {result['dscr10220_count']} rows"
        )

        for item in result["dscr10220"]:
            lines.append("")
            lines.append("-" * 100)
            lines.append(f"ROW INDEX {item['index']}")
            lines.append("-" * 100)

            lines.append("[INTERESTING FIELDS]")
            lines.append(
                json.dumps(
                    item["interesting_fields"],
                    ensure_ascii=False,
                    indent=2,
                )
            )

            lines.append("[ALL FIELDS]")
            lines.append(
                json.dumps(
                    item["all_fields"],
                    ensure_ascii=False,
                    indent=2,
                )
            )

        lines.append("")
        lines.append("[dscr10230.LIST]")
        lines.append(
            json.dumps(
                result["dscr10230"],
                ensure_ascii=False,
                indent=2,
            )
        )

        lines.append("")
        lines.append("[selectSavPd]")
        lines.append(
            json.dumps(
                result["selectSavPd"],
                ensure_ascii=False,
                indent=2,
            )
        )

        lines.append("")
        lines.append("[COMPACT RATE VIEW]")

        for item in result["dscr10220"]:
            row = item["all_fields"]

            lines.append(
                f"row={item['index']} | "
                f"APLY_RATE={row.get('APLY_RATE')} | "
                f"APLY_RATE_STR={row.get('APLY_RATE_STR')} | "
                f"COMP_INT_RATE={row.get('COMP_INT_RATE')} | "
                f"COMP_INT_RATE_STR={row.get('COMP_INT_RATE_STR')} | "
                f"TERM={row.get('TERM')} | "
                f"CLASS_CD={row.get('CLASS_CD')}"
            )

    return "\n".join(lines)


def main():
    print("=" * 80)
    print("SBRateBot V5 Shinhan dscr10220 Structure Analyzer v9")
    print("=" * 80)

    if not INPUT.exists():
        print("입력 파일 없음:", INPUT)
        print("먼저 shinhan_rate_api_test_v7.py를 실행하세요.")
        return

    raw = json.loads(
        INPUT.read_text(encoding="utf-8")
    )

    results = {}

    for label in ("ISA", "IRP"):
        print()
        print(f"[{label}] dscr10220 분석")

        result = analyze(
            label,
            raw.get(label, {}),
        )

        results[label] = result

        print(
            "  dscr10220 rows:",
            result["dscr10220_count"],
        )

        for item in result["dscr10220"]:
            row = item["all_fields"]

            print(
                f"  row {item['index']}: "
                f"APLY_RATE={row.get('APLY_RATE')} | "
                f"COMP_INT_RATE={row.get('COMP_INT_RATE')} | "
                f"TERM={row.get('TERM')} | "
                f"CLASS_CD={row.get('CLASS_CD')}"
            )

    OUT_JSON.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUT_JSON.write_text(
        json.dumps(
            results,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    OUT_TXT.write_text(
        build_report(results),
        encoding="utf-8",
    )

    print()
    print("=" * 80)
    print("완료")
    print("=" * 80)
    print("JSON:", OUT_JSON)
    print("TXT :", OUT_TXT)
    print()
    print("※ isa_rates.json / irp_rates.json은 수정하지 않습니다.")
    print("※ TXT 결과를 확인하면 기간별 금리 매핑 규칙을 확정할 수 있습니다.")


if __name__ == "__main__":
    main()
