# -*- coding: utf-8 -*-
"""
SBRateBot V5 - SBI ISA 공식소스 조사 Probe v1

목적
- SBI ISA 금리를 운영 수집기에 넣기 전에 공식 홈페이지 구조를 조사
- 기존 isa_rates.json / irp_rates.json 절대 수정하지 않음
- HTML / form / script / iframe / 링크 / 숫자 주변 문맥을 조사
- 결과를 TXT + JSON으로 저장

실행:
    cd C:\SBRateBot_V5
    py crawler\sbi_isa_probe_v1.py

출력:
    data\sbi_isa_probe_v1.txt
    data\sbi_isa_probe_v1.json
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

OUT_TXT = DATA_DIR / "sbi_isa_probe_v1.txt"
OUT_JSON = DATA_DIR / "sbi_isa_probe_v1.json"

START_URL = "https://www.sbisb.co.kr/gds0010100.act"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.7,en;q=0.6",
}

KEYWORDS = (
    "ISA",
    "개인종합자산관리",
    "정기예금",
    "금리",
    "이율",
    "적용금리",
    "약정금리",
    "3개월",
    "6개월",
    "12개월",
    "24개월",
    "36개월",
    "기준일",
    "시행일",
    "적용일",
    "변경일",
    "공시일",
)

URL_HINTS = (
    "isa",
    "gds",
    "prd",
    "product",
    "deposit",
    "dpst",
    "rate",
    "intr",
    "interest",
    "ajax",
    "json",
    "api",
    "detail",
    "view",
)

RATE_RE = re.compile(
    r"(?<!\d)([0-9](?:\.[0-9]{1,3})?)\s*%"
)

TERM_RE = re.compile(
    r"(3|6|12|24|36)\s*(?:개월|month)",
    re.I,
)

DATE_RE = re.compile(
    r"20\d{2}\s*(?:[-./년]\s*)\d{1,2}\s*(?:[-./월]\s*)\d{1,2}\s*(?:일)?"
)


def clean(value):
    return re.sub(
        r"\s+",
        " ",
        str(value or "")
    ).strip()


def context(text, pos, radius=220):
    return text[
        max(0, pos-radius):
        min(len(text), pos+radius)
    ]


def fetch(session, url, method="GET", data=None):
    if method == "POST":
        r = session.post(
            url,
            data=data,
            timeout=20,
            allow_redirects=True,
        )
    else:
        r = session.get(
            url,
            timeout=20,
            allow_redirects=True,
        )

    r.raise_for_status()

    if not r.encoding or r.encoding.lower() == "iso-8859-1":
        r.encoding = r.apparent_encoding or "utf-8"

    return r


def inspect_page(session, url):
    r = fetch(
        session,
        url,
    )

    html = r.text
    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    page_text = " ".join(
        soup.stripped_strings
    )

    keyword_contexts = []

    for keyword in KEYWORDS:
        start = 0

        while True:
            pos = page_text.lower().find(
                keyword.lower(),
                start,
            )

            if pos < 0:
                break

            keyword_contexts.append({
                "keyword": keyword,
                "context": context(
                    page_text,
                    pos,
                ),
            })

            start = pos + len(keyword)

            if sum(
                1
                for x in keyword_contexts
                if x["keyword"] == keyword
            ) >= 10:
                break

    rate_contexts = []

    for m in RATE_RE.finditer(
        page_text
    ):
        rate_contexts.append({
            "rate": m.group(1),
            "context": context(
                page_text,
                m.start(),
            ),
        })

        if len(rate_contexts) >= 100:
            break

    term_contexts = []

    for m in TERM_RE.finditer(
        page_text
    ):
        term_contexts.append({
            "term": m.group(1) + "개월",
            "context": context(
                page_text,
                m.start(),
            ),
        })

        if len(term_contexts) >= 100:
            break

    date_contexts = []

    for m in DATE_RE.finditer(
        page_text
    ):
        date_contexts.append({
            "date": m.group(0),
            "context": context(
                page_text,
                m.start(),
            ),
        })

        if len(date_contexts) >= 50:
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

        if any(
            hint in combined
            for hint in URL_HINTS
        ) or "ISA" in label.upper():
            links.append({
                "text": label,
                "url": href,
            })

    scripts = []

    for script in soup.find_all(
        "script"
    ):
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

        script_text = clean(
            script.get_text(
                " ",
                strip=True,
            )
        )

        if not script_text:
            continue

        low = script_text.lower()

        if (
            "isa" in low
            or "ajax" in low
            or "$.post" in low
            or "$.get" in low
            or "fetch(" in low
            or ".act" in low
            or "json" in low
        ):
            scripts.append({
                "type": "inline",
                "text": script_text[:10000],
            })

    iframes = []

    for iframe in soup.find_all(
        "iframe",
        src=True,
    ):
        iframes.append(
            urljoin(
                r.url,
                iframe.get("src"),
            )
        )

    return {
        "requested_url": url,
        "final_url": r.url,
        "status_code": r.status_code,
        "content_type": r.headers.get(
            "Content-Type"
        ),
        "title": clean(
            soup.title.string
            if soup.title
            else ""
        ),
        "keyword_contexts": keyword_contexts,
        "rate_contexts": rate_contexts,
        "term_contexts": term_contexts,
        "date_contexts": date_contexts,
        "forms": forms,
        "links": links[:200],
        "scripts": scripts[:200],
        "iframes": iframes,
    }


def candidate_urls(result):
    urls = []

    for item in result.get(
        "links",
        []
    ):
        url = item.get("url")

        if not url:
            continue

        combined = (
            url
            + " "
            + clean(item.get("text"))
        ).lower()

        if (
            "isa" in combined
            or "정기예금" in combined
            or "금리" in combined
            or "이율" in combined
        ):
            urls.append(url)

    for iframe in result.get(
        "iframes",
        []
    ):
        urls.append(iframe)

    unique = []

    for url in urls:
        if url not in unique:
            unique.append(url)

    return unique[:20]


def make_report(data):
    lines = []

    def add(value=""):
        lines.append(
            str(value)
        )

    add("=" * 100)
    add("SBRateBot V5 - SBI ISA 공식소스 조사 Probe v1")
    add("=" * 100)
    add(
        "실행시각: "
        + data["generated_at"]
    )
    add("금리 JSON 수정: NO")
    add()

    for idx, page in enumerate(
        data.get("pages", []),
        1,
    ):
        add("=" * 100)
        add(
            f"PAGE {idx}: "
            f"{page.get('final_url')}"
        )
        add("=" * 100)
        add(
            "TITLE: "
            + clean(
                page.get("title")
            )
        )
        add(
            "HTTP: "
            + str(
                page.get("status_code")
            )
        )
        add()

        add(
            f"[KEYWORD CONTEXTS] "
            f"{len(page.get('keyword_contexts', []))}"
        )

        for row in page.get(
            "keyword_contexts",
            []
        )[:120]:
            add(
                f"- {row.get('keyword')}: "
                f"{row.get('context')}"
            )

        add()
        add(
            f"[TERM CONTEXTS] "
            f"{len(page.get('term_contexts', []))}"
        )

        for row in page.get(
            "term_contexts",
            []
        )[:80]:
            add(
                f"- {row.get('term')}: "
                f"{row.get('context')}"
            )

        add()
        add(
            f"[RATE CONTEXTS] "
            f"{len(page.get('rate_contexts', []))}"
        )

        for row in page.get(
            "rate_contexts",
            []
        )[:80]:
            add(
                f"- {row.get('rate')}%: "
                f"{row.get('context')}"
            )

        add()
        add(
            f"[DATE CONTEXTS] "
            f"{len(page.get('date_contexts', []))}"
        )

        for row in page.get(
            "date_contexts",
            []
        )[:50]:
            add(
                f"- {row.get('date')}: "
                f"{row.get('context')}"
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
        add("[LINKS]")

        for link in page.get(
            "links",
            []
        )[:100]:
            add(
                f"- {link.get('text')} | "
                f"{link.get('url')}"
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
        )[:80]:
            if script.get("type") == "external":
                add(
                    "- EXTERNAL: "
                    + script.get("url", "")
                )
            else:
                add(
                    "- INLINE: "
                    + script.get("text", "")
                )

        add()

    if data.get("errors"):
        add("=" * 100)
        add("ERRORS")
        add("=" * 100)

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
    print("=" * 80)
    print("SBI ISA 공식소스 조사 Probe v1")
    print("=" * 80)

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
        "start_url": START_URL,
        "pages": [],
        "errors": [],
    }

    try:
        first = inspect_page(
            session,
            START_URL,
        )

        output["pages"].append(
            first
        )

        print(
            "[1] 조사:",
            first.get("final_url")
        )

        for url in candidate_urls(
            first
        ):
            if url == first.get(
                "final_url"
            ):
                continue

            try:
                print(
                    "[추가 조사]",
                    url
                )

                page = inspect_page(
                    session,
                    url,
                )

                output["pages"].append(
                    page
                )

            except Exception as e:
                output["errors"].append({
                    "url": url,
                    "error": repr(e),
                })

    except Exception as e:
        output["errors"].append({
            "url": START_URL,
            "error": repr(e),
        })

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
