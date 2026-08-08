# SBRateBot V5 - Shinhan Cached Bundle Analyzer v3
# ------------------------------------------------------------
# 목적:
#   인터넷 재다운로드 없이 이미 저장된
#   data/shinhan_bundle_cache/main.ceea2362.js
#   파일만 분석한다.
#
# 추적 대상:
#   PD_0080 = ISA정기예금
#   PD_0081 = 퇴직연금 정기예금
#
# 분석 내용:
#   1) route export 심볼 찾기 (예: PD_0080:()=>aN)
#   2) 해당 심볼 정의 위치 찾기
#   3) 주변 webpack module/chunk 참조 추출
#   4) API/action/data key 후보 추출
#   5) 결과 JSON + 사람이 보기 쉬운 TXT 저장
#
# 실행:
#   python crawler/shinhan_cached_bundle_analyzer_v3.py
#
# 결과:
#   data/shinhan_cached_analysis_v3.json
#   data/shinhan_cached_analysis_v3.txt

import json
import re
from datetime import datetime
from pathlib import Path


CACHE = Path("data/shinhan_bundle_cache/main.ceea2362.js")

OUT_JSON = Path("data/shinhan_cached_analysis_v3.json")
OUT_TXT = Path("data/shinhan_cached_analysis_v3.txt")

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


def unique(values):
    out = []
    seen = set()

    for value in values:
        if value and value not in seen:
            seen.add(value)
            out.append(value)

    return out


def get_context(text, index, radius=5000):
    left = max(0, index - radius)
    right = min(len(text), index + radius)
    return text[left:right]


def find_all(text, needle, limit=100):
    indexes = []
    start = 0

    while len(indexes) < limit:
        idx = text.find(needle, start)

        if idx < 0:
            break

        indexes.append(idx)
        start = idx + max(1, len(needle))

    return indexes


def find_export_symbol(text, view_id):
    """
    예:
    PD_0080:()=>aN
    PD_0081:()=>iN
    """
    patterns = [
        rf'{re.escape(view_id)}:\(\)=>\$?([A-Za-z_$][A-Za-z0-9_$]*)',
        rf'{re.escape(view_id)}\s*:\s*\(\)\s*=>\s*\$?([A-Za-z_$][A-Za-z0-9_$]*)',
    ]

    for pattern in patterns:
        m = re.search(pattern, text)

        if m:
            return m.group(1), m.start()

    return None, None


def find_symbol_definitions(text, symbol, limit=30):
    """
    minified bundle에서 다음 형태를 폭넓게 탐색:
      const aN=
      let aN=
      var aN=
      ,aN=
      ;aN=
    """
    patterns = [
        rf'\bconst\s+{re.escape(symbol)}\s*=',
        rf'\blet\s+{re.escape(symbol)}\s*=',
        rf'\bvar\s+{re.escape(symbol)}\s*=',
        rf'[,;]{re.escape(symbol)}\s*=',
    ]

    results = []

    for pattern in patterns:
        for m in re.finditer(pattern, text):
            results.append(m.start())

            if len(results) >= limit:
                return sorted(unique(results))

    return sorted(unique(results))


def extract_module_ids(context):
    """
    webpack module require 후보:
      n(12345)
      t(12345)
      e(12345)
    """
    ids = re.findall(
        r'\b[A-Za-z_$][A-Za-z0-9_$]*\((\d{2,7})\)',
        context,
    )

    return unique(ids)


def extract_chunk_ids(context):
    """
    webpack lazy chunk 후보:
      n.e(1234)
      t.e(1234)
      Promise.all([n.e(1),n.e(2)])
    """
    ids = re.findall(
        r'\.[e]\((\d{1,7})\)',
        context,
    )

    return unique(ids)


def extract_action_strings(context):
    quoted = re.findall(
        r'["\']([^"\']{3,300})["\']',
        context,
    )

    keys = (
        "SELECT",
        "REQUEST",
        "PRODUCT",
        "DEPOSIT",
        "SAVING",
        "RATE",
        "INTEREST",
        "INTR",
        "GOODS",
        "PRD",
        "PD0080",
        "PD0081",
        "PD_0080",
        "PD_0081",
        "ISA",
        "IRP",
        "퇴직연금",
        "정기예금",
    )

    return unique(
        value
        for value in quoted
        if any(key.lower() in value.lower() for key in keys)
    )


def extract_api_paths(context):
    quoted = re.findall(
        r'["\']([^"\']{2,500})["\']',
        context,
    )

    paths = []

    for value in quoted:
        low = value.lower()

        if (
            "/api/" in low
            or low.startswith("api/")
            or ".do" in low
            or "select_" in low
            or "request_" in low
        ):
            paths.append(value)

    return unique(paths)


def extract_function_calls(context):
    """
    주변의 'foo.bar(...)', 'foo(...)' 형태를 대략 추출.
    너무 많은 일반 호출을 줄이기 위해 상품/조회 문맥 키워드 포함 호출 우선.
    """
    calls = re.findall(
        r'([A-Za-z_$][A-Za-z0-9_$]*(?:\.[A-Za-z_$][A-Za-z0-9_$]*){0,2})\(',
        context,
    )

    blocked = {
        "if",
        "for",
        "while",
        "switch",
        "catch",
        "function",
        "return",
        "Math",
        "Object",
        "Array",
        "JSON",
        "String",
        "Number",
    }

    return unique(
        c for c in calls
        if c.split(".")[0] not in blocked
    )[:300]


def analyze_target(text, label, meta):
    view_id = meta["view_id"]

    symbol, export_pos = find_export_symbol(
        text,
        view_id,
    )

    result = {
        "view_id": view_id,
        "name": meta["name"],
        "export_symbol": symbol,
        "export_position": export_pos,
        "view_occurrences": find_all(text, view_id, limit=50),
        "definitions": [],
    }

    # route export 주변 문맥도 저장
    if export_pos is not None:
        route_context = get_context(
            text,
            export_pos,
            radius=2500,
        )

        result["route_context"] = route_context
        result["route_module_ids"] = extract_module_ids(route_context)
        result["route_chunk_ids"] = extract_chunk_ids(route_context)
        result["route_actions"] = extract_action_strings(route_context)
        result["route_api_paths"] = extract_api_paths(route_context)

    if not symbol:
        return result

    def_positions = find_symbol_definitions(
        text,
        symbol,
        limit=30,
    )

    for pos in def_positions:
        context = get_context(
            text,
            pos,
            radius=12000,
        )

        result["definitions"].append({
            "position": pos,
            "context": context,
            "module_ids": extract_module_ids(context),
            "chunk_ids": extract_chunk_ids(context),
            "actions": extract_action_strings(context),
            "api_paths": extract_api_paths(context),
            "function_calls": extract_function_calls(context),
        })

    return result


def write_txt(result):
    lines = []

    lines.append("=" * 80)
    lines.append("SBRateBot V5 Shinhan Cached Bundle Analyzer v3")
    lines.append("=" * 80)
    lines.append(f"cache: {result['cache_file']}")
    lines.append(f"bytes: {result['cache_bytes']:,}")
    lines.append("")

    for label in ("ISA", "IRP"):
        data = result["targets"][label]

        lines.append("=" * 80)
        lines.append(
            f"{label} / {data['view_id']} / {data['name']}"
        )
        lines.append("=" * 80)

        lines.append(
            f"export symbol: {data.get('export_symbol')}"
        )
        lines.append(
            f"view occurrences: {len(data.get('view_occurrences', []))}"
        )
        lines.append(
            f"definition count: {len(data.get('definitions', []))}"
        )

        if data.get("route_module_ids"):
            lines.append(
                "route module ids: "
                + ", ".join(data["route_module_ids"])
            )

        if data.get("route_chunk_ids"):
            lines.append(
                "route chunk ids: "
                + ", ".join(data["route_chunk_ids"])
            )

        if data.get("route_actions"):
            lines.append("")
            lines.append("[ROUTE ACTION 후보]")
            for value in data["route_actions"][:100]:
                lines.append(" - " + value)

        if data.get("route_api_paths"):
            lines.append("")
            lines.append("[ROUTE API/PATH 후보]")
            for value in data["route_api_paths"][:100]:
                lines.append(" - " + value)

        for idx, definition in enumerate(
            data.get("definitions", []),
            start=1,
        ):
            lines.append("")
            lines.append("-" * 80)
            lines.append(
                f"[DEFINITION #{idx}] position={definition['position']}"
            )

            if definition["module_ids"]:
                lines.append(
                    "module ids: "
                    + ", ".join(definition["module_ids"][:100])
                )

            if definition["chunk_ids"]:
                lines.append(
                    "chunk ids: "
                    + ", ".join(definition["chunk_ids"][:100])
                )

            if definition["actions"]:
                lines.append("[ACTION 후보]")
                for value in definition["actions"][:100]:
                    lines.append(" - " + value)

            if definition["api_paths"]:
                lines.append("[API/PATH 후보]")
                for value in definition["api_paths"][:100]:
                    lines.append(" - " + value)

            lines.append("[CONTEXT]")
            lines.append(definition["context"])

        lines.append("")

    OUT_TXT.parent.mkdir(parents=True, exist_ok=True)
    OUT_TXT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main():
    print("=" * 72)
    print("SBRateBot V5 Shinhan Cached Bundle Analyzer v3")
    print("=" * 72)

    if not CACHE.exists():
        print()
        print("캐시 파일을 찾지 못했습니다.")
        print("필요 파일:")
        print(f"  {CACHE}")
        print()
        print(
            "먼저 shinhan_isa_irp_probe_v2.py를 실행해 "
            "main.ceea2362.js를 받아주세요."
        )
        return

    raw = CACHE.read_bytes()
    text = raw.decode(
        "utf-8",
        errors="replace",
    )

    print(
        f"캐시 로드: {CACHE} "
        f"({len(raw):,} bytes)"
    )

    result = {
        "bank": "신한저축은행",
        "analyzed_at": datetime.now().isoformat(
            timespec="seconds"
        ),
        "cache_file": str(CACHE),
        "cache_bytes": len(raw),
        "targets": {},
    }

    for label, meta in TARGETS.items():
        print()
        print(
            f"[{label}] {meta['view_id']} 분석 중..."
        )

        data = analyze_target(
            text,
            label,
            meta,
        )

        result["targets"][label] = data

        print(
            "  export symbol:",
            data.get("export_symbol"),
        )
        print(
            "  occurrences:",
            len(data.get("view_occurrences", [])),
        )
        print(
            "  definitions:",
            len(data.get("definitions", [])),
        )

        for idx, definition in enumerate(
            data.get("definitions", []),
            start=1,
        ):
            print(
                f"  definition#{idx}"
                f" module_ids={definition['module_ids'][:12]}"
                f" chunk_ids={definition['chunk_ids'][:12]}"
            )

            if definition["api_paths"]:
                print(
                    "    API/PATH:",
                    definition["api_paths"][:10],
                )

            if definition["actions"]:
                print(
                    "    ACTION:",
                    definition["actions"][:10],
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

    write_txt(result)

    print()
    print("=" * 72)
    print("완료")
    print("=" * 72)
    print("JSON:", OUT_JSON)
    print("TXT :", OUT_TXT)
    print()
    print(
        "다음에는 TXT 파일 내용을 보내주면 "
        "실제 상품 데이터 호출 코드를 더 좁힐 수 있습니다."
    )


if __name__ == "__main__":
    main()
