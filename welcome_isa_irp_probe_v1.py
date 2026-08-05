# -*- coding: utf-8 -*-
"""
SBRateBot V5 - 웰컴저축은행 ISA + IRP 통합 조사 Probe v1

목적
- 웰컴저축은행 공식 홈페이지에서 ISA/퇴직연금(IRP) 상품과 금리 구조를 한 번에 조사
- 기존 isa_rates.json / irp_rates.json 절대 수정하지 않음
- 상품명, 기간(3/6/12/24/36개월), 금리, 기준일/공시일 후보,
  링크/form/script/iframe/API 단서를 TXT + JSON으로 저장

실행:
    cd C:\SBRateBot_V5
    py crawler\welcome_isa_irp_probe_v1.py

출력:
    data\welcome_isa_irp_probe_v1.txt
    data\welcome_isa_irp_probe_v1.json
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

OUT_TXT = DATA_DIR / "welcome_isa_irp_probe_v1.txt"
OUT_JSON = DATA_DIR / "welcome_isa_irp_probe_v1.json"

# 웰컴저축은행 공식 사이트 진입점.
START_URLS = [
    "https://www.welcomebank.co.kr/",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.7,en;q=0.6",
}

PRODUCT_KEYWORDS = (
    "ISA",
    "개인종합자산관리",
    "퇴직연금",
    "IRP",
    "정기예금",
    "원리금보장",
    "원리금보장형",
)

RATE_KEYWORDS = (
    "금리",
    "이율",
    "적용금리",
    "약정금리",
    "기본금리",
    "연이율",
    "세전",
)

DATE_KEYWORDS = (
    "기준일",
    "현재",
    "시행일",
    "적용일",
    "변경일",
    "금리변경일",
    "공시일",
)

TERM_RE = re.compile(
    r"(?<!\d)(3|6|12|24|36)\s*(?:개월|month)",
    re.I,
)

RATE_RE = re.compile(
    r"(?<!\d)([0-9](?:\.[0-9]{1,3})?)\s*%"
)

DATE_RE = re.compile(
    r"20\d{2}\s*(?:[-./년]\s*)"
    r"\d{1,2}\s*(?:[-./월]\s*)"
    r"\d{1,2}\s*(?:일)?"
)

URL_HINTS = (
    "isa", "irp", "retire", "pension",
    "product", "prd", "deposit", "dpst",
    "rate", "interest", "intr",
    "ajax", "api", "json",
    "view", "detail",
)


def clean(value):
    return re.sub(
        r"\s+",
        " ",
        str(value or "")
    ).strip()


def clip(text, pos, radius=260):
    return text[
        max(0, pos-radius):
        min(len(text), pos+radius)
    ]


def fetch(session, url):
    r = session.get(
        url,
        timeout=20,
        allow_redirects=True,
    )
    r.raise_for_status()

    if not r.encoding or r.encoding.lower() == "iso-8859-1":
        r.encoding = r.apparent_encoding or "utf-8"

    return r


def keyword_contexts(text, keywords, limit_each=12):
    rows = []

    for keyword in keywords:
        start = 0
        count = 0

        while count < limit_each:
            pos = text.lower().find(
                keyword.lower(),
                start,
            )

            if pos < 0:
                break

            rows.append({
                "keyword": keyword,
                "context": clip(
                    text,
                    pos,
                ),
            })

            start = pos + len(keyword)
            count += 1

    return rows


def inspect_page(session, url):
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

    product_contexts = keyword_contexts(
        page_text,
        PRODUCT_KEYWORDS,
    )

    rate_keyword_contexts = keyword_contexts(
        page_text,
        RATE_KEYWORDS,
    )

    date_keyword_contexts = keyword_contexts(
        page_text,
        DATE_KEYWORDS,
    )

    term_contexts = []

    for m in TERM_RE.finditer(
        page_text
    ):
        term_contexts.append({
            "term": m.group(1) + "개월",
            "context": clip(
                page_text,
                m.start(),
            ),
        })

        if len(term_contexts) >= 150:
            break

    rate_contexts = []

    for m in RATE_RE.finditer(
        page_text
    ):
        rate_contexts.append({
            "rate": m.group(1),
            "context": clip(
                page_text,
                m.start(),
            ),
        })

        if len(rate_contexts) >= 150:
            break

    date_contexts = []

    for m in DATE_RE.finditer(
        page_text
    ):
        date_contexts.append({
            "date": m.group(0),
            "context": clip(
                page_text,
                m.start(),
            ),
        })

        if len(date_contexts) >= 100:
            break

    links = []

    for a in soup.find_all(
        "a",
        href=True,
    ):
        href = urljoin(
            r.url,
            a.get("href"),
        )
        label = clean(
            a.get_text(
                " ",
                strip=True,
            )
        )

        combined = (
            href + " " + label
        ).lower()

        if (
            any(
                word.lower() in combined
                for word in PRODUCT_KEYWORDS
            )
            or any(
                hint in combined
                for hint in URL_HINTS
            )
        ):
            links.append({
                "text": label,
                "url": href,
            })

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

    iframes = [
        urljoin(
            r.url,
            iframe.get("src"),
        )
        for iframe in soup.find_all(
            "iframe",
            src=True,
        )
    ]

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
            "isa" in low
            or "irp" in low
            or "퇴직연금" in body
            or "ajax" in low
            or "fetch(" in low
            or "$.post" in low
            or "$.get" in low
            or "json" in low
            or "/api/" in low
        ):
            scripts.append({
                "type": "inline",
                "text": body[:15000],
            })

    return {
        "requested_url": url,
        "final_url": r.url,
        "status_code": r.status_code,
        "title": clean(
            soup.title.string
            if soup.title
            else ""
        ),
        "product_contexts": product_contexts,
        "rate_keyword_contexts": rate_keyword_contexts,
        "date_keyword_contexts": date_keyword_contexts,
        "term_contexts": term_contexts,
        "rate_contexts": rate_contexts,
        "date_contexts": date_contexts,
        "links": links[:300],
        "forms": forms,
        "iframes": iframes,
        "scripts": scripts[:300],
    }


def relevant_candidate_urls(page):
    candidates = []

    for item in page.get(
        "links",
        []
    ):
        url = item.get("url")
        label = clean(
            item.get("text")
        )

        if not url:
            continue

        combined = (
            url + " " + label
        ).lower()

        strong = (
            "isa" in combined
            or "irp" in combined
            or "퇴직연금" in combined
            or "개인종합자산관리" in combined
        )

        if strong:
            candidates.append(url)

    for iframe in page.get(
        "iframes",
        []
    ):
        candidates.append(iframe)

    unique = []

    for url in candidates:
        if url not in unique:
            unique.append(url)

    return unique[:30]


def classify_contexts(page):
    """
    결과 확인을 쉽게 하기 위한 단순 분류.
    실제 운영 데이터에는 사용하지 않는다.
    """
    joined = " ".join(
        row.get("context", "")
        for row in (
            page.get("product_contexts", [])
            + page.get("term_contexts", [])
            + page.get("rate_contexts", [])
        )
    )

    return {
        "has_isa_text": (
            "ISA" in joined.upper()
            or "개인종합자산관리" in joined
        ),
        "has_irp_text": (
            "IRP" in joined.upper()
            or "퇴직연금" in joined
        ),
        "has_term_text": bool(
            page.get("term_contexts")
        ),
        "has_rate_text": bool(
            page.get("rate_contexts")
        ),
        "has_date_text": bool(
            page.get("date_contexts")
        ),
    }


def make_report(data):
    lines = []

    def add(value=""):
        lines.append(
            str(value)
        )

    add("=" * 110)
    add("SBRateBot V5 - 웰컴저축은행 ISA + IRP 통합 조사 Probe v1")
    add("=" * 110)
    add(
        "실행시각: "
        + data["generated_at"]
    )
    add("isa_rates.json / irp_rates.json 수정: NO")
    add()

    for idx, page in enumerate(
        data.get("pages", []),
        1,
    ):
        add("=" * 110)
        add(
            f"PAGE {idx}: "
            f"{page.get('final_url')}"
        )
        add("=" * 110)
        add(
            "TITLE: "
            + clean(
                page.get("title")
            )
        )
        add(
            "CLASSIFY: "
            + json.dumps(
                page.get(
                    "classification",
                    {}
                ),
                ensure_ascii=False,
            )
        )
        add()

        groups = [
            (
                "PRODUCT",
                page.get(
                    "product_contexts",
                    []
                ),
            ),
            (
                "RATE KEYWORD",
                page.get(
                    "rate_keyword_contexts",
                    []
                ),
            ),
            (
                "TERM",
                page.get(
                    "term_contexts",
                    []
                ),
            ),
            (
                "RATE",
                page.get(
                    "rate_contexts",
                    []
                ),
            ),
            (
                "DATE KEYWORD",
                page.get(
                    "date_keyword_contexts",
                    []
                ),
            ),
            (
                "DATE",
                page.get(
                    "date_contexts",
                    []
                ),
            ),
        ]

        for name, rows in groups:
            add(
                f"[{name}] {len(rows)}"
            )

            for row in rows[:120]:
                label = (
                    row.get("keyword")
                    or row.get("term")
                    or row.get("rate")
                    or row.get("date")
                    or "-"
                )

                add(
                    f"- {label}: "
                    f"{row.get('context', '')}"
                )

            add()

        add("[LINKS]")

        for item in page.get(
            "links",
            []
        )[:150]:
            add(
                f"- {item.get('text')} | "
                f"{item.get('url')}"
            )

        add()
        add("[FORMS]")

        for form in page.get(
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
        add("[IFRAMES]")

        for iframe in page.get(
            "iframes",
            []
        ):
            add(
                "- " + iframe
            )

        add()
        add("[SCRIPTS]")

        for script in page.get(
            "scripts",
            []
        )[:100]:
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
        add("=" * 110)
        add("ERRORS")
        add("=" * 110)

        for error in data["errors"]:
            add(
                json.dumps(
                    error,
                    ensure_ascii=False,
                )
            )

    return "\n".join(
        lines
    )


def main():
    print("=" * 90)
    print("웰컴저축은행 ISA + IRP 통합 조사 Probe v1")
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
        "pages": [],
        "errors": [],
    }

    visited = set()
    queue = list(
        START_URLS
    )

    while queue and len(visited) < 35:
        url = queue.pop(0)

        if url in visited:
            continue

        visited.add(url)

        try:
            print(
                "[조사]",
                url
            )

            page = inspect_page(
                session,
                url,
            )

            page["classification"] = classify_contexts(
                page
            )

            output["pages"].append(
                page
            )

            for candidate in relevant_candidate_urls(
                page
            ):
                if (
                    candidate not in visited
                    and candidate not in queue
                ):
                    queue.append(
                        candidate
                    )

        except Exception as e:
            output["errors"].append({
                "url": url,
                "error": repr(e),
            })

            print(
                "[ERROR]",
                url,
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
    print("기존 금리 JSON은 수정하지 않았습니다.")


if __name__ == "__main__":
    main()
