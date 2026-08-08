# SBRateBot V5 - Shinhan Cached Bundle Analyzer v4
# ------------------------------------------------------------
# v3에서 export symbol(aN / iN)은 찾았지만 definition=0 이었던 문제 보완.
#
# 핵심 변경:
# - aN= / iN= 형태를 단순 문자열 기반으로 전부 탐색
# - 함수 선언, 화살표 함수, 콤마 체인, 객체 할당 형태 폭넓게 탐색
# - export 심볼의 모든 등장 위치 주변 문맥 분석
# - 각 위치 주변 module id / chunk id / API/action 후보 추출
#
# 실행:
#   python crawler/shinhan_cached_bundle_analyzer_v4.py
#
# 결과:
#   data/shinhan_cached_analysis_v4.json
#   data/shinhan_cached_analysis_v4.txt

import json
import re
from datetime import datetime
from pathlib import Path


CACHE = Path("data/shinhan_bundle_cache/main.ceea2362.js")
OUT_JSON = Path("data/shinhan_cached_analysis_v4.json")
OUT_TXT = Path("data/shinhan_cached_analysis_v4.txt")

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


def positions(text, needle, limit=200):
    out = []
    start = 0

    while len(out) < limit:
        idx = text.find(needle, start)

        if idx < 0:
            break

        out.append(idx)
        start = idx + max(1, len(needle))

    return out


def context(text, pos, radius=10000):
    return text[
        max(0, pos - radius):
        min(len(text), pos + radius)
    ]


def find_export_symbol(text, view_id):
    patterns = [
        rf'{re.escape(view_id)}:\(\)=>([A-Za-z_$][A-Za-z0-9_$]*)',
        rf'{re.escape(view_id)}\s*:\s*\(\)\s*=>\s*([A-Za-z_$][A-Za-z0-9_$]*)',
    ]

    for pattern in patterns:
        m = re.search(pattern, text)

        if m:
            return m.group(1), m.start()

    return None, None


def symbol_assignment_positions(text, symbol):
    needles = [
        symbol + "=",
        "const " + symbol + "=",
        "let " + symbol + "=",
        "var " + symbol + "=",
        "function " + symbol + "(",
        "," + symbol + "=",
        ";" + symbol + "=",
    ]

    found = []

    for needle in needles:
        for pos in positions(text, needle, limit=100):
            found.append((pos, needle))

    found.sort(key=lambda x: x[0])

    # 동일/근접 위치 중복 제거
    result = []

    for pos, needle in found:
        if result and abs(pos - result[-1][0]) < 3:
            continue
        result.append((pos, needle))

    return result


def extract_module_ids(text):
    patterns = [
        r'\b[A-Za-z_$][A-Za-z0-9_$]*\((\d{2,7})\)',
        r'=\w+\((\d{2,7})\)',
    ]

    found = []

    for pattern in patterns:
        found.extend(
            re.findall(pattern, text)
        )

    return unique(found)


def extract_chunk_ids(text):
    found = re.findall(
        r'\.e\((\d{1,7})\)',
        text,
    )
    return unique(found)


def extract_strings(text):
    return re.findall(
        r'["\']([^"\']{2,500})["\']',
        text,
    )


def extract_api_action_candidates(text):
    strings = extract_strings(text)

    keys = (
        "/api/",
        "api/",
        ".do",
        "select",
        "request",
        "product",
        "deposit",
        "saving",
        "rate",
        "interest",
        "intr",
        "goods",
        "prd",
        "isa",
        "irp",
        "퇴직연금",
        "정기예금",
        "PD0080",
        "PD0081",
        "PD_0080",
        "PD_0081",
    )

    values = []

    for value in strings:
        low = value.lower()

        if any(key.lower() in low for key in keys):
            values.append(value)

    return unique(values)


def extract_urls(text):
    return unique(
        re.findall(
            r'https?://[^"\'\s<>\\]+',
            text,
            flags=re.I,
        )
    )


def classify_context(ctx, symbol):
    return {
        "module_ids": extract_module_ids(ctx),
        "chunk_ids": extract_chunk_ids(ctx),
        "urls": extract_urls(ctx),
        "candidates": extract_api_action_candidates(ctx),
        "contains_symbol_assignment": (
            symbol + "=" in ctx
            or "function " + symbol + "(" in ctx
        ),
    }


def analyze(text, label, meta):
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
        "view_positions": positions(
            text,
            view_id,
            limit=100,
        ),
        "symbol_positions": [],
        "assignment_positions": [],
    }

    if not symbol:
        return result

    # 심볼 모든 등장 위치
    for pos in positions(
        text,
        symbol,
        limit=300,
    ):
        ctx = context(
            text,
            pos,
            radius=7000,
        )

        info = classify_context(
            ctx,
            symbol,
        )

        result["symbol_positions"].append({
            "position": pos,
            "context": ctx,
            **info,
        })

    # 실제 할당 위치 후보
    assignments = symbol_assignment_positions(
        text,
        symbol,
    )

    for pos, matched_by in assignments:
        ctx = context(
            text,
            pos,
            radius=16000,
        )

        info = classify_context(
            ctx,
            symbol,
        )

        result["assignment_positions"].append({
            "position": pos,
            "matched_by": matched_by,
            "context": ctx,
            **info,
        })

    return result


def render_txt(result):
    lines = []

    lines.append("=" * 88)
    lines.append("SBRateBot V5 Shinhan Cached Bundle Analyzer v4")
    lines.append("=" * 88)
    lines.append(f"CACHE: {result['cache_file']}")
    lines.append(f"BYTES: {result['cache_bytes']:,}")
    lines.append("")

    for label in ("ISA", "IRP"):
        data = result["targets"][label]

        lines.append("=" * 88)
        lines.append(
            f"{label} / {data['view_id']} / {data['name']}"
        )
        lines.append("=" * 88)

        lines.append(
            f"EXPORT SYMBOL: {data.get('export_symbol')}"
        )
        lines.append(
            f"VIEW OCCURRENCES: {len(data.get('view_positions', []))}"
        )
        lines.append(
            f"SYMBOL OCCURRENCES: {len(data.get('symbol_positions', []))}"
        )
        lines.append(
            f"ASSIGNMENT CANDIDATES: {len(data.get('assignment_positions', []))}"
        )

        lines.append("")

        if data.get("assignment_positions"):
            lines.append("[ASSIGNMENT CANDIDATES]")

            for i, item in enumerate(
                data["assignment_positions"],
                1,
            ):
                lines.append("-" * 88)
                lines.append(
                    f"#{i} POSITION={item['position']} "
                    f"MATCH={item['matched_by']}"
                )
                lines.append(
                    "MODULE_IDS="
                    + ", ".join(item["module_ids"][:100])
                )
                lines.append(
                    "CHUNK_IDS="
                    + ", ".join(item["chunk_ids"][:100])
                )

                if item["candidates"]:
                    lines.append("[API/ACTION/STRING 후보]")
                    for x in item["candidates"][:150]:
                        lines.append(" - " + x)

                lines.append("[CONTEXT]")
                lines.append(item["context"])
                lines.append("")

        else:
            lines.append(
                "[!] 직접 assignment를 못 찾음. "
                "심볼 등장 위치를 분석합니다."
            )

            for i, item in enumerate(
                data.get("symbol_positions", [])[:20],
                1,
            ):
                lines.append("-" * 88)
                lines.append(
                    f"[SYMBOL OCCURRENCE #{i}] "
                    f"POSITION={item['position']}"
                )
                lines.append(
                    "MODULE_IDS="
                    + ", ".join(item["module_ids"][:80])
                )
                lines.append(
                    "CHUNK_IDS="
                    + ", ".join(item["chunk_ids"][:80])
                )

                if item["candidates"]:
                    lines.append("[API/ACTION/STRING 후보]")
                    for x in item["candidates"][:100]:
                        lines.append(" - " + x)

                lines.append("[CONTEXT]")
                lines.append(item["context"])
                lines.append("")

    OUT_TXT.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main():
    print("=" * 72)
    print("SBRateBot V5 Shinhan Cached Bundle Analyzer v4")
    print("=" * 72)

    if not CACHE.exists():
        print("캐시 파일 없음:", CACHE)
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
            f"[{label}] {meta['view_id']} 분석"
        )

        data = analyze(
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
            "  symbol occurrences:",
            len(data.get("symbol_positions", [])),
        )
        print(
            "  assignment candidates:",
            len(data.get("assignment_positions", [])),
        )

        for i, item in enumerate(
            data.get("assignment_positions", [])[:10],
            1,
        ):
            print(
                f"    #{i} pos={item['position']} "
                f"match={item['matched_by']}"
            )
            print(
                "       modules:",
                item["module_ids"][:15],
            )
            print(
                "       chunks :",
                item["chunk_ids"][:15],
            )
            print(
                "       candidates:",
                item["candidates"][:10],
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

    render_txt(result)

    print()
    print("=" * 72)
    print("완료")
    print("=" * 72)
    print("JSON:", OUT_JSON)
    print("TXT :", OUT_TXT)


if __name__ == "__main__":
    main()
