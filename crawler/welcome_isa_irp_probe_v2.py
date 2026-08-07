# -*- coding: utf-8 -*-
"""
SBRateBot V5 - 웰컴저축은행 ISA + IRP 직결 조사 Probe v2

사용자가 확인한 웰컴저축은행 공식 상품 상세 URL에 직접 접속하여
ISA / 퇴직연금(IRP)의 기간별 금리와 공시일/기준일 후보를 조사한다.

주의:
- 기존 isa_rates.json / irp_rates.json 수정하지 않음
- 조사 결과만 TXT + JSON으로 저장

실행:
    cd C:\SBRateBot_V5
    py crawler\welcome_isa_irp_probe_v2.py

출력:
    data\welcome_isa_irp_probe_v2.txt
    data\welcome_isa_irp_probe_v2.json
"""

import json
import re
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

OUT_TXT = DATA_DIR / "welcome_isa_irp_probe_v2.txt"
OUT_JSON = DATA_DIR / "welcome_isa_irp_probe_v2.json"

TARGETS = {
    "ISA": (
        "https://www.welcomebank.co.kr/ib20/mnu/IBNFPMDSP001"
        "?ib20_wc=IBNFPMDSP001_00:IBNFPMCMN001_00"
        "&prdCd=1120255020&sysDsCd=01"
    ),
    "IRP": (
        "https://www.welcomebank.co.kr/ib20/mnu/IBNFPMDSP001"
        "?ib20_wc=IBNFPMDSP001_00:IBNFPMCMN001_00"
        "&prdCd=1120255021&sysDsCd=01"
    ),
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.7,en;q=0.6",
    "Referer": "https://www.welcomebank.co.kr/",
}

TERMS = ("3", "6", "12", "24", "36")

TERM_RE = re.compile(
    r"(?<!\d)(3|6|12|24|36)\s*(?:개월|month)",
    re.I,
)

RATE_RE = re.compile(
    r"(?<![\d.])([0-9](?:\.[0-9]{1,3})?)\s*%"
)

DATE_RE = re.compile(
    r"(20\d{2})\s*[-./년]\s*"
    r"(\d{1,2})\s*[-./월]\s*"
    r"(\d{1,2})\s*(?:일)?"
)

DATE_WORDS = (
    "기준일",
    "현재",
    "공시일",
    "시행일",
    "적용일",
    "변경일",
    "금리변경일",
)

RATE_WORDS = (
    "금리",
    "이율",
    "적용금리",
    "약정금리",
    "기본금리",
    "세전",
)

PRODUCT_WORDS = (
    "ISA",
    "개인종합자산관리",
    "퇴직연금",
    "IRP",
    "정기예금",
    "원리금보장",
)


def clean(value):
    return re.sub(
        r"\s+",
        " ",
        str(value or "")
    ).strip()


def clip(text, pos, radius=300):
    return text[
        max(0, pos-radius):
        min(len(text), pos+radius)
    ]


def fetch(session, url):
    r = session.get(
        url,
        timeout=25,
        allow_redirects=True,
    )
    r.raise_for_status()

    if not r.encoding or r.encoding.lower() == "iso-8859-1":
        r.encoding = r.apparent_encoding or "utf-8"

    return r


def contexts_for_words(text, words, limit_each=15):
    rows = []

    for word in words:
        start = 0
        count = 0

        while count < limit_each:
            pos = text.lower().find(
                word.lower(),
                start,
            )

            if pos < 0:
                break

            rows.append({
                "keyword": word,
                "context": clip(
                    text,
                    pos,
                ),
            })

            start = pos + len(word)
            count += 1

    return rows


def extract_tables(soup):
    tables = []

    for idx, table in enumerate(
        soup.find_all("table"),
        1,
    ):
        rows = []

        for tr in table.find_all("tr"):
            cells = [
                clean(
                    cell.get_text(
                        " ",
                        strip=True,
                    )
                )
                for cell in tr.find_all(
                    ["th", "td"]
                )
            ]

            if cells:
                rows.append(cells)

        if rows:
            tables.append({
                "index": idx,
                "text": clean(
                    table.get_text(
                        " ",
                        strip=True,
                    )
                ),
                "rows": rows,
            })

    return tables


def extract_term_rate_candidates(text):
    """
    기간과 %가 가까이 붙어 있는 문맥을 조사한다.
    자동 확정이 아니라 후보 생성용.
    """
    candidates = []

    for term_match in TERM_RE.finditer(text):
        term = term_match.group(1)
        window = text[
            max(0, term_match.start()-180):
            min(len(text), term_match.end()+300)
        ]

        rates = [
            float(m.group(1))
            for m in RATE_RE.finditer(window)
            if 0 <= float(m.group(1)) <= 20
        ]

        candidates.append({
            "term": term + "개월",
            "rates_nearby": rates[:15],
            "context": window,
        })

    return candidates[:150]


def inspect_target(session, category, url):
    r = fetch(
        session,
        url,
    )

    soup = BeautifulSoup(
        r.text,
        "html.parser",
    )

    page_text = " ".join(
        soup.stripped_strings
    )

    tables = extract_tables(
        soup
    )

    product_contexts = contexts_for_words(
        page_text,
        PRODUCT_WORDS,
    )

    rate_keyword_contexts = contexts_for_words(
        page_text,
        RATE_WORDS,
    )

    date_keyword_contexts = contexts_for_words(
        page_text,
        DATE_WORDS,
    )

    term_rate_candidates = extract_term_rate_candidates(
        page_text
    )

    rate_contexts = []

    for m in RATE_RE.finditer(
        page_text
    ):
        value = float(
            m.group(1)
        )

        if 0 <= value <= 20:
            rate_contexts.append({
                "rate": value,
                "context": clip(
                    page_text,
                    m.start(),
                ),
            })

        if len(rate_contexts) >= 200:
            break

    date_contexts = []

    for m in DATE_RE.finditer(
        page_text
    ):
        y, mn, d = map(
            int,
            m.groups()
        )

        date_contexts.append({
            "date": f"{y:04d}-{mn:02d}-{d:02d}",
            "raw": m.group(0),
            "context": clip(
                page_text,
                m.start(),
            ),
        })

        if len(date_contexts) >= 100:
            break

    forms = []

    for form in soup.find_all("form"):
        fields = []

        for tag in form.find_all(
            ["input", "select", "textarea"]
        ):
            fields.append({
                "tag": tag.name,
                "name": tag.get("name"),
                "id": tag.get("id"),
                "value": tag.get("value"),
                "type": tag.get("type"),
            })

        forms.append({
            "id": form.get("id"),
            "name": form.get("name"),
            "method": clean(
                form.get("method")
            ).upper() or "GET",
            "action": urljoin(
                r.url,
                form.get("action") or ""
            ),
            "fields": fields,
        })

    scripts = []

    for script in soup.find_all("script"):
        src = script.get("src")

        if src:
            scripts.append({
                "type": "external",
                "url": urljoin(
                    r.url,
                    src,
                ),
            })
            continue

        body = clean(
            script.get_text(
                " ",
                strip=True,
            )
        )

        if not body:
            continue

        low = body.lower()

        if (
            "1120255020" in body
            or "1120255021" in body
            or "prdcd" in low
            or "ajax" in low
            or "fetch(" in low
            or "$.post" in low
            or "$.get" in low
            or "json" in low
            or "rate" in low
            or "interest" in low
        ):
            scripts.append({
                "type": "inline",
                "text": body[:20000],
            })

    links = []

    for a in soup.find_all(
        "a",
        href=True,
    ):
        label = clean(
            a.get_text(
                " ",
                strip=True,
            )
        )
        href = urljoin(
            r.url,
            a.get("href"),
        )

        combined = (
            label + " " + href
        ).lower()

        if (
            "isa" in combined
            or "irp" in combined
            or "퇴직연금" in combined
            or "금리" in combined
            or "이율" in combined
            or "prdcd" in combined
        ):
            links.append({
                "text": label,
                "url": href,
            })

    return {
        "category": category,
        "requested_url": url,
        "final_url": r.url,
        "status_code": r.status_code,
        "title": clean(
            soup.title.string
            if soup.title
            else ""
        ),
        "page_text_length": len(page_text),
        "product_contexts": product_contexts,
        "rate_keyword_contexts": rate_keyword_contexts,
        "date_keyword_contexts": date_keyword_contexts,
        "term_rate_candidates": term_rate_candidates,
        "rate_contexts": rate_contexts,
        "date_contexts": date_contexts,
        "tables": tables,
        "forms": forms,
        "scripts": scripts[:300],
        "links": links[:200],
    }


def make_report(data):
    lines = []

    def add(value=""):
        lines.append(
            str(value)
        )

    add("=" * 115)
    add("SBRateBot V5 - 웰컴저축은행 ISA + IRP 직결 조사 Probe v2")
    add("=" * 115)
    add(
        "실행시각: "
        + data["generated_at"]
    )
    add("기존 금리 JSON 수정: NO")
    add()

    for category in (
        "ISA",
        "IRP",
    ):
        item = data.get(
            category,
            {}
        )

        add("=" * 115)
        add(category)
        add("=" * 115)
        add(
            "URL: "
            + clean(
                item.get("final_url")
            )
        )
        add(
            "TITLE: "
            + clean(
                item.get("title")
            )
        )
        add(
            "HTTP: "
            + str(
                item.get("status_code")
            )
        )
        add(
            "TEXT LENGTH: "
            + str(
                item.get("page_text_length")
            )
        )
        add()

        add("[기간별 금리 후보]")

        for row in item.get(
            "term_rate_candidates",
            []
        ):
            add(
                f"- {row.get('term')} | "
                f"rates={row.get('rates_nearby')}"
            )
            add(
                "  "
                + row.get(
                    "context",
                    ""
                )
            )

        add()
        add("[금리 % 문맥]")

        for row in item.get(
            "rate_contexts",
            []
        )[:120]:
            add(
                f"- {row.get('rate')}% | "
                f"{row.get('context')}"
            )

        add()
        add("[공시일/날짜 후보]")

        for row in item.get(
            "date_contexts",
            []
        )[:80]:
            add(
                f"- {row.get('date')} "
                f"({row.get('raw')}) | "
                f"{row.get('context')}"
            )

        add()
        add("[날짜 키워드 문맥]")

        for row in item.get(
            "date_keyword_contexts",
            []
        )[:80]:
            add(
                f"- {row.get('keyword')} | "
                f"{row.get('context')}"
            )

        add()
        add("[상품명/상품구조 문맥]")

        for row in item.get(
            "product_contexts",
            []
        )[:80]:
            add(
                f"- {row.get('keyword')} | "
                f"{row.get('context')}"
            )

        add()
        add("[TABLES]")

        for table in item.get(
            "tables",
            []
        ):
            add(
                f"--- TABLE {table.get('index')} ---"
            )

            for row in table.get(
                "rows",
                []
            ):
                add(
                    " | ".join(row)
                )

        add()
        add("[FORMS]")

        for form in item.get(
            "forms",
            []
        ):
            add(
                json.dumps(
                    form,
                    ensure_ascii=False,
                )
            )

        add()
        add("[LINKS]")

        for link in item.get(
            "links",
            []
        )[:100]:
            add(
                f"- {link.get('text')} | "
                f"{link.get('url')}"
            )

        add()
        add("[SCRIPTS]")

        for script in item.get(
            "scripts",
            []
        )[:120]:
            if script.get("type") == "external":
                add(
                    "- EXTERNAL: "
                    + script.get(
                        "url",
                        ""
                    )
                )
            else:
                add(
                    "- INLINE: "
                    + script.get(
                        "text",
                        ""
                    )
                )

        add()

    if data.get("errors"):
        add("=" * 115)
        add("ERRORS")
        add("=" * 115)

        for row in data["errors"]:
            add(
                json.dumps(
                    row,
                    ensure_ascii=False,
                )
            )

    return "\n".join(
        lines
    )


def main():
    print("=" * 90)
    print("웰컴저축은행 ISA + IRP 직결 조사 Probe v2")
    print("=" * 90)

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    session = requests.Session()
    session.headers.update(
        HEADERS
    )

    output = {
        "generated_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "source": "웰컴저축은행 공식 상품 상세페이지",
        "ISA": {},
        "IRP": {},
        "errors": [],
    }

    for category, url in TARGETS.items():
        try:
            print(
                f"[{category}] 조사:",
                url
            )

            output[category] = inspect_target(
                session,
                category,
                url,
            )

        except Exception as e:
            output["errors"].append({
                "category": category,
                "url": url,
                "error": repr(e),
            })

            print(
                f"[{category} ERROR]",
                repr(e)
            )

    OUT_JSON.write_text(
        json.dumps(
            output,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    OUT_TXT.write_text(
        make_report(
            output
        ),
        encoding="utf-8",
    )

    print()
    print("완료")
    print("TXT :", OUT_TXT)
    print("JSON:", OUT_JSON)
    print("※ isa_rates.json / irp_rates.json은 수정하지 않았습니다.")


if __name__ == "__main__":
    main()
