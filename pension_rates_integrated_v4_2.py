# ============================================
# SBRateBot V5
# ISA / IRP Target Rate Collector v4.2 + KoreaInvest Integrated
# crawler/pension_rates.py
#
# 1차 대상:
# - data/target_banks.json 의 targets_deduped
#
# 입력:
# - data/latest_rates.json
# - data/target_banks.json
# - data/pension_sources.json (있으면 재사용)
#
# 출력:
# - data/pension_sources.json
# - data/isa_rates.json
# - data/irp_rates.json
#
# 목표:
# - 타깃은행만 집중 탐색
# - ISA / IRP 후보 URL 확보
# - 3/6/12/24/36개월 금리 추출
# - 확신 낮은 값은 review_required
# ============================================

import json
import re
import ssl
import sys
import time
from collections import deque
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse, urldefrag

import requests
import urllib3
from bs4 import BeautifulSoup


# ============================================
# PATH
# ============================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

LATEST_RATES_FILE = DATA_DIR / "latest_rates.json"
TARGET_BANKS_FILE = DATA_DIR / "target_banks.json"
PENSION_SOURCES_FILE = DATA_DIR / "pension_sources.json"

ISA_RATES_FILE = DATA_DIR / "isa_rates.json"
IRP_RATES_FILE = DATA_DIR / "irp_rates.json"


# ============================================
# SETTINGS
# ============================================

REQUEST_TIMEOUT = 15
REQUEST_DELAY = 0.12

MAX_DEPTH = 4
MAX_PAGES_PER_BANK = 60
MAX_LINKS_PER_PAGE = 700

TARGET_PERIODS = [3, 6, 12, 24, 36]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/142.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,*/*;q=0.8"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.7,en;q=0.5",
}


# ============================================
# KEYWORDS
# ============================================

ISA_KEYWORDS = [
    "ISA",
    "개인종합자산관리계좌",
    "개인종합자산관리",
    "중개형ISA",
    "신탁형ISA",
    "일임형ISA",
    "ISA정기예금",
    "ISA 정기예금",
    "ISA전용",
    "ISA 전용",
]

IRP_KEYWORDS = [
    "IRP",
    "개인형퇴직연금",
    "개인형 퇴직연금",
    "퇴직연금",
    "퇴직 연금",
    "원리금보장",
    "원리금 보장",
    "원리금보장상품",
    "퇴직연금정기예금",
    "퇴직연금 정기예금",
    "DC형",
    "DB형",
]

NAVIGATION_KEYWORDS = [
    "예금",
    "예금상품",
    "수신",
    "수신상품",
    "상품",
    "상품안내",
    "금융상품",
    "개인금융",
    "퇴직연금",
    "연금",
    "IRP",
    "ISA",
    "공시",
    "상품공시",
    "금리",
    "정기예금",
]

IGNORE_TEXT_KEYWORDS = [
    "로그인",
    "회원가입",
    "인증센터",
    "고객센터",
    "채용",
    "회사소개",
    "오시는길",
    "개인정보",
    "보안",
    "대출",
    "신용대출",
    "담보대출",
]


# ============================================
# HTTP
# ============================================

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

ssl._create_default_https_context = ssl._create_unverified_context

session = requests.Session()
session.headers.update(HEADERS)


# ============================================
# COMMON
# ============================================

def clean_text(value):
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def load_json(path, default=None):
    if not path.exists():
        return default

    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2,
        )


def normalize_url(url):
    url = clean_text(url)

    if not url:
        return ""

    url = (
        url.replace("&amp;", "&")
        .replace("\\/", "/")
        .strip("'\" ")
    )

    if url.startswith("//"):
        url = "https:" + url

    if not re.match(r"^https?://", url, re.I):
        return url

    url, _ = urldefrag(url)

    return url


def absolute_url(base_url, value):
    value = normalize_url(value)

    if not value:
        return ""

    if re.match(r"^https?://", value, re.I):
        result = value
    else:
        result = urljoin(base_url, value)

    result, _ = urldefrag(result)

    return result


def canonical_url(url):
    url = normalize_url(url)

    if not re.match(r"^https?://", url, re.I):
        return url

    parsed = urlparse(url)

    scheme = parsed.scheme.lower()
    host = parsed.netloc.lower()

    if host.endswith(":80") and scheme == "http":
        host = host[:-3]

    if host.endswith(":443") and scheme == "https":
        host = host[:-4]

    path = parsed.path or "/"

    if path != "/":
        path = path.rstrip("/")

    query = parsed.query

    return (
        f"{scheme}://{host}{path}"
        + (f"?{query}" if query else "")
    )


def normalize_host(url):
    try:
        host = urlparse(url).netloc.lower().split(":")[0]

        if host.startswith("www."):
            host = host[4:]

        return host

    except Exception:
        return ""


def same_domain(base_url, target_url):
    base_host = normalize_host(base_url)
    target_host = normalize_host(target_url)

    if not base_host or not target_host:
        return False

    return (
        target_host == base_host
        or target_host.endswith("." + base_host)
        or base_host.endswith("." + target_host)
    )


def is_http_url(url):
    return bool(
        re.match(
            r"^https?://",
            str(url or ""),
            re.I,
        )
    )


# ============================================
# TARGET BANKS
# ============================================

def load_target_banks():
    data = load_json(
        TARGET_BANKS_FILE,
        {},
    )

    if isinstance(data, dict):
        targets = data.get(
            "targets_deduped",
            [],
        )

    elif isinstance(data, list):
        targets = data

    else:
        targets = []

    targets = [
        clean_text(x)
        for x in targets
        if clean_text(x)
    ]

    if not targets:
        raise ValueError(
            "target_banks.json의 targets_deduped가 비어 있습니다."
        )

    return targets


# ============================================
# BANK MASTER
# ============================================

def extract_bank_homepages():
    raw = load_json(
        LATEST_RATES_FILE,
        [],
    )

    if not isinstance(raw, list):
        raise ValueError(
            "latest_rates.json 구조를 확인해주세요."
        )

    banks = {}

    for item in raw:
        if not isinstance(item, dict):
            continue

        bank = clean_text(
            item.get("bank")
        )

        homepage = normalize_url(
            item.get("homepage")
        )

        if (
            bank
            and homepage
            and is_http_url(homepage)
            and bank not in banks
        ):
            banks[bank] = homepage

    return banks


# ============================================
# FETCH
# ============================================

def fetch_html(url):
    try:
        response = session.get(
            url,
            timeout=REQUEST_TIMEOUT,
            verify=False,
            allow_redirects=True,
        )

        response.raise_for_status()

        if not response.encoding:
            response.encoding = response.apparent_encoding

        text = response.text

        content_type = response.headers.get(
            "Content-Type",
            "",
        ).lower()

        if (
            "html" not in content_type
            and "<html" not in text[:2000].lower()
        ):
            return None, response.url, "not_html"

        return text, response.url, None

    except requests.RequestException as e:
        return None, url, str(e)


# ============================================
# SCORING
# ============================================

def keyword_score(text, keywords):
    normalized = clean_text(text).lower()
    score = 0

    for keyword in keywords:
        k = keyword.lower()

        if k in normalized:
            if len(k) >= 7:
                score += 14
            elif len(k) >= 4:
                score += 9
            else:
                score += 5

    return score


def navigation_score(text):
    normalized = clean_text(text).lower()

    for bad in IGNORE_TEXT_KEYWORDS:
        if bad.lower() in normalized:
            return -100

    score = keyword_score(
        normalized,
        NAVIGATION_KEYWORDS,
    )

    score += (
        keyword_score(
            normalized,
            ISA_KEYWORDS,
        )
        * 2
    )

    score += (
        keyword_score(
            normalized,
            IRP_KEYWORDS,
        )
        * 2
    )

    return score


# ============================================
# URL EXTRACTION
# ============================================

def extract_urls_from_javascript(text):
    text = str(text or "")

    found = []

    patterns = [
        r"""['"]((?:https?:)?//[^'"]+)['"]""",
        r"""['"]((?:/|\.\.?/)[^'"]+\.(?:do|act|jsp|php|html?|aspx?)(?:\?[^'"]*)?)['"]""",
        r"""['"]((?:/|\.\.?/)[^'"]*(?:product|deposit|saving|pension|irp|isa|retire)[^'"]*)['"]""",
    ]

    for pattern in patterns:
        for match in re.findall(
            pattern,
            text,
            flags=re.I,
        ):
            if match not in found:
                found.append(match)

    return found[:150]


def add_candidate(
    store,
    homepage,
    current_url,
    raw_url,
    context="",
    source="href",
):
    raw_url = clean_text(raw_url)

    if not raw_url:
        return

    if raw_url.lower().startswith(
        ("mailto:", "tel:", "data:", "#")
    ):
        return

    url = absolute_url(
        current_url,
        raw_url,
    )

    if not is_http_url(url):
        return

    if not same_domain(
        homepage,
        url,
    ):
        return

    key = canonical_url(url)

    combined = " ".join(
        [
            clean_text(context),
            raw_url,
            url,
        ]
    )

    item = {
        "url": url,
        "key": key,
        "context": clean_text(context)[:300],
        "source": source,
        "nav_score": navigation_score(combined),
        "isa_score": keyword_score(
            combined,
            ISA_KEYWORDS,
        ),
        "irp_score": keyword_score(
            combined,
            IRP_KEYWORDS,
        ),
    }

    old = store.get(key)

    if old is None:
        store[key] = item
        return

    old_score = (
        old["nav_score"]
        + old["isa_score"]
        + old["irp_score"]
    )

    new_score = (
        item["nav_score"]
        + item["isa_score"]
        + item["irp_score"]
    )

    if new_score > old_score:
        store[key] = item


def extract_links(
    current_url,
    homepage,
    html,
):
    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    candidates = {}

    # a
    for tag in soup.find_all(
        "a",
        limit=MAX_LINKS_PER_PAGE,
    ):
        context = " ".join(
            [
                clean_text(
                    tag.get_text(
                        " ",
                        strip=True,
                    )
                ),
                clean_text(
                    tag.get("title")
                ),
                clean_text(
                    tag.get("aria-label")
                ),
            ]
        )

        href = clean_text(
            tag.get("href")
        )

        if href and not href.lower().startswith(
            "javascript:"
        ):
            add_candidate(
                candidates,
                homepage,
                current_url,
                href,
                context,
                "href",
            )

        onclick = clean_text(
            tag.get("onclick")
        )

        if onclick:
            for raw in extract_urls_from_javascript(
                onclick
            ):
                add_candidate(
                    candidates,
                    homepage,
                    current_url,
                    raw,
                    context + " " + onclick,
                    "onclick",
                )

    # iframe/frame
    for tag in soup.find_all(
        ["iframe", "frame"],
        src=True,
    ):
        add_candidate(
            candidates,
            homepage,
            current_url,
            tag.get("src"),
            clean_text(
                tag.get("title")
            ),
            "iframe",
        )

    # form
    for tag in soup.find_all(
        "form",
        action=True,
    ):
        add_candidate(
            candidates,
            homepage,
            current_url,
            tag.get("action"),
            clean_text(
                tag.get("name")
            ),
            "form",
        )

    # onclick/data attributes
    for tag in soup.find_all(
        ["button", "div", "li", "span"],
    ):
        context = clean_text(
            tag.get_text(
                " ",
                strip=True,
            )
        )[:250]

        for attr in (
            "data-url",
            "data-href",
            "data-link",
            "data-page",
        ):
            value = tag.get(attr)

            if value:
                add_candidate(
                    candidates,
                    homepage,
                    current_url,
                    value,
                    context,
                    attr,
                )

        onclick = tag.get(
            "onclick"
        )

        if onclick:
            for raw in extract_urls_from_javascript(
                onclick
            ):
                add_candidate(
                    candidates,
                    homepage,
                    current_url,
                    raw,
                    context + " " + str(onclick),
                    "onclick",
                )

    # script
    for script in soup.find_all(
        "script"
    ):
        script_text = script.get_text(
            "\n",
            strip=False,
        )

        if not script_text:
            continue

        lower = script_text.lower()

        if not (
            any(
                k.lower() in lower
                for k in NAVIGATION_KEYWORDS
            )
            or "location" in lower
            or "window.open" in lower
            or "href" in lower
        ):
            continue

        for raw in extract_urls_from_javascript(
            script_text
        ):
            pos = script_text.find(
                raw
            )

            context = (
                script_text[
                    max(0, pos - 160):
                    min(
                        len(script_text),
                        pos + len(raw) + 160,
                    )
                ]
                if pos >= 0
                else ""
            )

            add_candidate(
                candidates,
                homepage,
                current_url,
                raw,
                context,
                "script",
            )

    return (
        soup,
        list(
            candidates.values()
        ),
    )


# ============================================
# SOURCE DISCOVERY
# ============================================

def page_text(soup):
    try:
        copy = BeautifulSoup(
            str(soup),
            "html.parser",
        )

        for bad in copy(
            ["script", "style", "noscript"]
        ):
            bad.extract()

        return clean_text(
            copy.get_text(
                " ",
                strip=True,
            )
        )[:15000]

    except Exception:
        return ""


def page_scores(
    soup,
    url,
):
    text = page_text(
        soup
    )

    combined = (
        url
        + " "
        + text
    )

    lower = combined.lower()

    isa_score = keyword_score(
        combined,
        ISA_KEYWORDS,
    )

    irp_score = keyword_score(
        combined,
        IRP_KEYWORDS,
    )

    if (
        "isa" in lower
        and (
            "예금" in lower
            or "금리" in lower
            or "이율" in lower
        )
    ):
        isa_score += 20

    if (
        "퇴직연금" in lower
        and (
            "예금" in lower
            or "원리금" in lower
            or "금리" in lower
            or "이율" in lower
        )
    ):
        irp_score += 22

    if (
        "irp" in lower
        and (
            "예금" in lower
            or "원리금" in lower
            or "금리" in lower
            or "이율" in lower
        )
    ):
        irp_score += 18

    return (
        isa_score,
        irp_score,
    )



def is_homepage_only(url, homepage):
    try:
        a = urlparse(canonical_url(url))
        b = urlparse(canonical_url(homepage))

        a_path = (a.path or "/").rstrip("/") or "/"
        b_path = (b.path or "/").rstrip("/") or "/"

        return (
            normalize_host(url) == normalize_host(homepage)
            and a_path == b_path
            and not a.query
        )
    except Exception:
        return False


def discover_source(
    bank,
    homepage,
    kind,
):
    queue = deque(
        [
            (
                homepage,
                0,
                100,
            )
        ]
    )

    visited = set()

    best = None

    while (
        queue
        and len(visited) < MAX_PAGES_PER_BANK
    ):
        current_url, depth, priority = queue.popleft()

        key = canonical_url(
            current_url
        )

        if key in visited:
            continue

        if depth > MAX_DEPTH:
            continue

        visited.add(
            key
        )

        html, final_url, error = fetch_html(
            current_url
        )

        if html is None:
            continue

        current_url = normalize_url(
            final_url
        )

        soup, links = extract_links(
            current_url,
            homepage,
            html,
        )

        isa_score, irp_score = page_scores(
            soup,
            current_url,
        )

        score = (
            isa_score
            if kind == "isa"
            else irp_score
        )

        if (
            score >= 12
            and not is_homepage_only(
                current_url,
                homepage,
            )
        ):
            candidate = {
                "url": current_url,
                "score": score,
                "depth": depth,
                "visited_pages": len(
                    visited
                ),
            }

            if (
                best is None
                or candidate["score"]
                > best["score"]
            ):
                best = candidate

        if depth < MAX_DEPTH:
            next_links = []

            for link in links:
                score2 = (
                    link["nav_score"]
                    + link["isa_score"]
                    + link["irp_score"]
                )

                if depth == 0 and score2 <= 0:
                    continue

                if depth > 0 and score2 < 0:
                    continue

                next_links.append(
                    (
                        link["url"],
                        score2,
                    )
                )

            next_links.sort(
                key=lambda x: x[1],
                reverse=True,
            )

            for next_url, next_score in next_links[:20]:
                next_key = canonical_url(
                    next_url
                )

                if next_key not in visited:
                    queue.append(
                        (
                            next_url,
                            depth + 1,
                            next_score,
                        )
                    )

        time.sleep(
            REQUEST_DELAY
        )

    return best


# ============================================
# RATE EXTRACTION
# ============================================

def parse_rate_number(value):
    if value is None:
        return None

    text = clean_text(value)

    match = re.search(
        r"(?<!\d)(\d{1,2}(?:\.\d{1,3})?)\s*%",
        text,
    )

    if not match:
        return None

    try:
        rate = float(
            match.group(1)
        )

        if 0.1 <= rate <= 10.0:
            return rate

    except Exception:
        pass

    return None


def extract_period_rate_pairs(text):
    """
    텍스트에서 기간별 금리를 찾는다.

    중요:
    - 반드시 % 기호가 있는 값만 금리로 인정
    - '3개월', '6개월', '12개월'의 숫자 자체를
      금리로 오인하지 않도록 숫자-only 패턴은 사용하지 않음
    """

    results = {
        period: []
        for period in TARGET_PERIODS
    }

    normalized = (
        str(text or "")
        .replace("\xa0", " ")
    )

    for period in TARGET_PERIODS:
        patterns = [
            # 12개월 ... 연 3.76%
            rf"{period}\s*개월[^0-9%]{{0,60}}(?:연\s*)?(\d{{1,2}}(?:\.\d{{1,3}})?)\s*%",

            # 12개월 ... 3.76 %
            rf"{period}\s*개월[\s\S]{{0,80}}?(\d{{1,2}}(?:\.\d{{1,3}})?)\s*%",

            # 3.76% ... 12개월
            rf"(\d{{1,2}}(?:\.\d{{1,3}})?)\s*%[\s\S]{{0,60}}?{period}\s*개월",
        ]

        for pattern in patterns:
            for match in re.findall(
                pattern,
                normalized,
                flags=re.I,
            ):
                try:
                    value = float(match)

                    # 저축은행 예금금리 현실 범위 필터
                    # 0.1% 미만 / 10% 초과는 오탐 가능성이 높음
                    if (
                        0.1 <= value <= 10.0
                        and value not in results[period]
                    ):
                        results[period].append(value)

                except Exception:
                    pass

    return results

def extract_table_rates(soup):
    """
    HTML table에서 기간-금리 구조 탐색.
    """

    results = {
        period: []
        for period in TARGET_PERIODS
    }

    for table in soup.find_all(
        "table"
    ):
        rows = table.find_all(
            "tr"
        )

        for row in rows:
            cells = [
                clean_text(
                    cell.get_text(
                        " ",
                        strip=True,
                    )
                )
                for cell in row.find_all(
                    ["th", "td"]
                )
            ]

            if not cells:
                continue

            joined = " | ".join(
                cells
            )

            for period in TARGET_PERIODS:
                if re.search(
                    rf"{period}\s*개월",
                    joined,
                ):
                    # 같은 행의 %값 모두
                    values = re.findall(
                        r"(?<!\d)(\d{1,2}(?:\.\d{1,3})?)\s*%",
                        joined,
                    )

                    for value in values:
                        try:
                            rate = float(
                                value
                            )

                            if (
                                0.1 <= rate <= 10.0
                                and rate not in results[
                                    period
                                ]
                            ):
                                results[
                                    period
                                ].append(
                                    rate
                                )

                        except Exception:
                            pass

    return results


def choose_rate(values):
    """
    한 기간에 여러 값이 있으면 우선 최고금리 사용.
    단, 자동수집임을 status에 남긴다.
    """

    clean_values = []

    for value in values:
        try:
            number = float(
                value
            )

            if (
                0.1 <= number <= 10.0
                and number not in clean_values
            ):
                clean_values.append(
                    number
                )

        except Exception:
            pass

    if not clean_values:
        return None

    return round(
        max(clean_values),
        3,
    )


def extract_rates_from_page(
    bank,
    kind,
    url,
):
    html, final_url, error = fetch_html(
        url
    )

    if html is None:
        return {
            "bank": bank,
            "category": kind.upper(),
            "source_url": url,
            "status": "fetch_error",
            "error": error,
            "rates": {
                f"{p}m": None
                for p in TARGET_PERIODS
            },
        }

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    text = soup.get_text(
        "\n",
        strip=True,
    )

    text_results = extract_period_rate_pairs(
        text
    )

    table_results = extract_table_rates(
        soup
    )

    rates = {}

    evidence = {}

    found_count = 0

    for period in TARGET_PERIODS:
        values = []

        values.extend(
            text_results.get(
                period,
                [],
            )
        )

        values.extend(
            table_results.get(
                period,
                [],
            )
        )

        values = list(
            dict.fromkeys(
                values
            )
        )

        selected = choose_rate(
            values
        )

        rates[
            f"{period}m"
        ] = selected

        evidence[
            f"{period}m"
        ] = values[:8]

        if selected is not None:
            found_count += 1

    # 상품명 추정
    product_name = None

    for selector in (
        "h1",
        "h2",
        "h3",
        ".title",
        ".tit",
        ".product-title",
        ".product_name",
    ):
        tag = soup.select_one(
            selector
        )

        if tag:
            value = clean_text(
                tag.get_text(
                    " ",
                    strip=True,
                )
            )

            if value:
                product_name = value[:120]
                break

    # 상태
    if found_count >= 3:
        status = "auto_extracted"

    elif found_count >= 1:
        status = "review_required"

    else:
        status = "rate_not_found"

    return {
        "bank": bank,
        "category": kind.upper(),
        "product": product_name,
        "rates": rates,
        "status": status,
        "source_url": normalize_url(
            final_url
        ),
        "evidence_values": evidence,
        "updated_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
    }


# ============================================
# KOREA INVESTMENT SAVINGS BANK
# Selenium / WebSquare special collector
# ============================================

KOREAINVEST_TARGETS = {
    "ISA": {
        "menu_id": "PRD-PDS001-10",
        "url": "https://sb.koreainvestment.com/?PRD-PDS001-10#",
        "expected_title": "ISA정기예금",
    },
    "IRP": {
        "menu_id": "PRD-PDS001-11",
        "url": "https://sb.koreainvestment.com/?PRD-PDS001-11#",
        "expected_title": "퇴직연금정기예금",
    },
}


def is_koreainvest_bank(bank):
    value = clean_text(bank).replace(" ", "")
    return "한국투자" in value


def _ki_parse_rate(value):
    value = clean_text(value)

    match = re.search(
        r"(\d+(?:\.\d+)?)",
        value,
    )

    if not match:
        return None

    try:
        rate = float(
            match.group(1)
        )
    except ValueError:
        return None

    if 0 <= rate <= 20:
        return rate

    return None


def _ki_period(value):
    value = clean_text(value)

    match = re.search(
        r"(\d+)\s*개월",
        value,
    )

    if not match:
        return None

    return int(
        match.group(1)
    )


def _ki_reference_date(value):
    value = clean_text(value)

    match = re.search(
        r"(\d{4})\s*년\s*(\d{1,2})\s*월\s*(\d{1,2})\s*일",
        value,
    )

    if not match:
        return None

    y, m, d = map(
        int,
        match.groups(),
    )

    return (
        f"{y:04d}-{m:02d}-{d:02d}"
    )


def _ki_month_key(value):
    value = clean_text(value)

    match = re.search(
        r"(\d{4})\D+(\d{1,2})",
        value,
    )

    if not match:
        return (0, 0)

    return (
        int(match.group(1)),
        int(match.group(2)),
    )


def _ki_create_driver():
    """
    회사 PC 기준 Edge 우선.
    실패 시 Chrome 자동 전환.
    """
    edge_error = None

    try:
        from selenium import webdriver
        from selenium.webdriver.edge.options import (
            Options as EdgeOptions
        )

        options = EdgeOptions()

        options.add_argument(
            "--headless=new"
        )
        options.add_argument(
            "--disable-gpu"
        )
        options.add_argument(
            "--window-size=1600,1200"
        )
        options.add_argument(
            "--ignore-certificate-errors"
        )
        options.add_argument(
            "--disable-popup-blocking"
        )
        options.add_argument(
            "--disable-notifications"
        )

        driver = webdriver.Edge(
            options=options
        )

        driver.set_page_load_timeout(
            30
        )

        return driver, "Edge"

    except Exception as e:
        edge_error = e

    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import (
            Options as ChromeOptions
        )

        options = ChromeOptions()

        options.add_argument(
            "--headless=new"
        )
        options.add_argument(
            "--disable-gpu"
        )
        options.add_argument(
            "--window-size=1600,1200"
        )
        options.add_argument(
            "--ignore-certificate-errors"
        )
        options.add_argument(
            "--disable-popup-blocking"
        )
        options.add_argument(
            "--disable-notifications"
        )

        driver = webdriver.Chrome(
            options=options
        )

        driver.set_page_load_timeout(
            30
        )

        return driver, "Chrome"

    except Exception as chrome_error:
        raise RuntimeError(
            "한국투자 Selenium Driver 실행 실패 "
            f"/ Edge={repr(edge_error)} "
            f"/ Chrome={repr(chrome_error)}"
        )


def _ki_wait_for_page(
    driver,
    expected_title,
):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import (
        WebDriverWait
    )
    from selenium.webdriver.support import (
        expected_conditions as EC
    )

    wait = WebDriverWait(
        driver,
        30,
    )

    wait.until(
        EC.presence_of_element_located(
            (
                By.ID,
                "mf_wfm_contents_intrGridView",
            )
        )
    )

    wait.until(
        lambda d:
            expected_title
            in clean_text(d.title)
            or expected_title
            in clean_text(
                d.find_element(
                    By.TAG_NAME,
                    "body",
                ).text
            )
    )

    time.sleep(2)


def _ki_get_rate_section(driver):
    return driver.execute_script(
        r"""
        const root =
            document.getElementById(
                "mf_wfm_contents_intrGridView"
            );

        if (!root) {
            return null;
        }

        const tables =
            Array.from(
                root.querySelectorAll("table")
            );

        return {
            text:
                (root.innerText || "")
                .replace(/\s+/g, " ")
                .trim(),

            tables:
                tables.map(
                    (table, tableIndex) => ({
                        tableIndex,
                        rows:
                            Array.from(
                                table.querySelectorAll(
                                    "tr"
                                )
                            ).map(
                                row =>
                                    Array.from(
                                        row.querySelectorAll(
                                            "th, td"
                                        )
                                    ).map(
                                        cell => ({
                                            text:
                                                (
                                                    cell.innerText
                                                    || ""
                                                )
                                                .replace(
                                                    /\s+/g,
                                                    " "
                                                )
                                                .trim(),

                                            tag:
                                                cell.tagName,

                                            rowspan:
                                                cell.getAttribute(
                                                    "rowspan"
                                                )
                                                || "1",

                                            colspan:
                                                cell.getAttribute(
                                                    "colspan"
                                                )
                                                || "1"
                                        })
                                    )
                            )
                    })
                )
        };
        """
    )


def _ki_parse_isa(
    bank,
    section,
    source_url,
):
    if not section:
        raise ValueError(
            "한국투자 ISA 금리영역 미확인"
        )

    rates = {
        f"{p}m": None
        for p in TARGET_PERIODS
    }

    evidence = {
        f"{p}m": []
        for p in TARGET_PERIODS
    }

    for table in section.get(
        "tables",
        [],
    ):
        found = 0

        for row in table.get(
            "rows",
            [],
        ):
            texts = [
                clean_text(
                    cell.get("text")
                )
                for cell in row
            ]

            if len(texts) < 2:
                continue

            period = _ki_period(
                texts[0]
            )

            if period not in TARGET_PERIODS:
                continue

            rate = _ki_parse_rate(
                texts[1]
            )

            if rate is None:
                continue

            rates[
                f"{period}m"
            ] = rate

            evidence[
                f"{period}m"
            ].append(rate)

            found += 1

        if found >= 3:
            break

    found_count = sum(
        value is not None
        for value in rates.values()
    )

    status = (
        "auto_extracted"
        if found_count >= 3
        else "review_required"
    )

    return {
        "bank": bank,
        "category": "ISA",
        "product": "ISA정기예금",
        "rates": rates,
        "status": status,
        "source_url": source_url,
        "evidence_values": evidence,
        "reference_date":
            _ki_reference_date(
                section.get(
                    "text",
                    "",
                )
            ),
        "collector":
            "koreainvest_websquare_selenium",
        "updated_at":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
    }


def _ki_parse_irp(
    bank,
    section,
    source_url,
):
    if not section:
        raise ValueError(
            "한국투자 IRP 금리영역 미확인"
        )

    target_rows = []

    for table in section.get(
        "tables",
        [],
    ):
        rows = table.get(
            "rows",
            [],
        )

        joined = " ".join(
            clean_text(
                cell.get("text")
            )
            for row in rows
            for cell in row
        )

        if (
            "DC/IRP형" in joined
            and "DB형" in joined
        ):
            target_rows = rows
            break

    if not target_rows:
        raise ValueError(
            "한국투자 IRP 금리표 미확인"
        )

    period_month_rows = {}
    current_period = None

    for row in target_rows:
        cells = [
            cell
            for cell in row
            if cell.get("tag") == "TD"
        ]

        texts = [
            clean_text(
                cell.get("text")
            )
            for cell in cells
        ]

        if not texts:
            continue

        first_period = _ki_period(
            texts[0]
        )

        if first_period in TARGET_PERIODS:
            current_period = first_period

            if len(texts) < 4:
                continue

            rate_month = texts[1]
            dc_irp_rate = _ki_parse_rate(
                texts[2]
            )
            db_rate = _ki_parse_rate(
                texts[3]
            )

        else:
            if current_period is None:
                continue

            if len(texts) < 3:
                continue

            rate_month = texts[0]
            dc_irp_rate = _ki_parse_rate(
                texts[1]
            )
            db_rate = _ki_parse_rate(
                texts[2]
            )

        if (
            dc_irp_rate is None
            and db_rate is None
        ):
            continue

        period_month_rows.setdefault(
            current_period,
            [],
        ).append({
            "rate_month": rate_month,
            "dc_irp_rate": dc_irp_rate,
            "db_rate": db_rate,
        })

    rates = {
        f"{p}m": None
        for p in TARGET_PERIODS
    }

    db_rates = {
        f"{p}m": None
        for p in TARGET_PERIODS
    }

    monthly_detail = {}

    evidence = {
        f"{p}m": []
        for p in TARGET_PERIODS
    }

    for period in TARGET_PERIODS:
        monthly_rows = (
            period_month_rows.get(
                period,
                [],
            )
        )

        if not monthly_rows:
            continue

        latest = max(
            monthly_rows,
            key=lambda x:
                _ki_month_key(
                    x["rate_month"]
                )
        )

        rates[
            f"{period}m"
        ] = latest[
            "dc_irp_rate"
        ]

        db_rates[
            f"{period}m"
        ] = latest[
            "db_rate"
        ]

        monthly_detail[
            f"{period}m"
        ] = latest[
            "rate_month"
        ]

        if (
            latest["dc_irp_rate"]
            is not None
        ):
            evidence[
                f"{period}m"
            ].append(
                latest[
                    "dc_irp_rate"
                ]
            )

    found_count = sum(
        value is not None
        for value in rates.values()
    )

    status = (
        "auto_extracted"
        if found_count >= 3
        else "review_required"
    )

    return {
        "bank": bank,
        "category": "IRP",
        "product": "퇴직연금정기예금",
        # 기존 SBRateBot IRP 구조는 DC/IRP형을 대표 금리로 사용
        "rates": rates,
        # 한국투자는 DB형도 별도 제공하므로 추가 보존
        "db_rates": db_rates,
        "rate_months": monthly_detail,
        "status": status,
        "source_url": source_url,
        "evidence_values": evidence,
        "reference_date":
            _ki_reference_date(
                section.get(
                    "text",
                    "",
                )
            ),
        "collector":
            "koreainvest_websquare_selenium",
        "updated_at":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
    }


def collect_koreainvest(
    bank,
):
    driver = None

    try:
        driver, browser = (
            _ki_create_driver()
        )

        results = {}

        for kind, cfg in (
            KOREAINVEST_TARGETS.items()
        ):
            driver.get(
                cfg["url"]
            )

            _ki_wait_for_page(
                driver,
                cfg["expected_title"],
            )

            section = (
                _ki_get_rate_section(
                    driver
                )
            )

            if kind == "ISA":
                results["isa"] = (
                    _ki_parse_isa(
                        bank,
                        section,
                        cfg["url"],
                    )
                )

            else:
                results["irp"] = (
                    _ki_parse_irp(
                        bank,
                        section,
                        cfg["url"],
                    )
                )

        results["source"] = {
            "homepage":
                "https://sb.koreainvestment.com/",
            "isa_url":
                KOREAINVEST_TARGETS[
                    "ISA"
                ]["url"],
            "isa_status": "verified",
            "irp_url":
                KOREAINVEST_TARGETS[
                    "IRP"
                ]["url"],
            "irp_status": "verified",
            "collector":
                "koreainvest_websquare_selenium",
            "browser": browser,
            "updated_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
        }

        return results

    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass



# ============================================
# MAIN COLLECT
# ============================================

def collect():
    targets = load_target_banks()

    homepages = extract_bank_homepages()

    previous_sources = load_json(
        PENSION_SOURCES_FILE,
        {},
    )

    if not isinstance(
        previous_sources,
        dict,
    ):
        previous_sources = {}

    print("=" * 72)
    print(
        "SBRateBot V5 ISA / IRP Target Rate Collector v4.2"
    )
    print("=" * 72)

    print(
        "대상은행:",
        len(targets),
    )

    print(
        ", ".join(
            targets
        )
    )

    print()

    source_results = dict(
        previous_sources
    )

    isa_results = []
    irp_results = []

    for index, bank in enumerate(
        targets,
        start=1,
    ):
        homepage = homepages.get(
            bank
        )

        print(
            f"[{index}/{len(targets)}] {bank}"
        )

        # ------------------------------------
        # 한국투자저축은행 전용 WebSquare 수집
        # ------------------------------------
        if is_koreainvest_bank(bank):
            print(
                "  한국투자 전용 수집 : "
                "Selenium/WebSquare"
            )

            try:
                ki = collect_koreainvest(
                    bank
                )

                source_results[
                    bank
                ] = ki["source"]

                isa_results.append(
                    ki["isa"]
                )

                irp_results.append(
                    ki["irp"]
                )

                print(
                    "  ISA 금리 :",
                    ki["isa"]["rates"],
                    f"[{ki['isa']['status']}]",
                )

                print(
                    "  IRP DC/IRP :",
                    ki["irp"]["rates"],
                    f"[{ki['irp']['status']}]",
                )

                print(
                    "  IRP DB :",
                    ki["irp"].get(
                        "db_rates",
                        {},
                    ),
                )

            except Exception as e:
                print(
                    "  한국투자 전용 수집 실패:",
                    repr(e),
                )

                source_results[
                    bank
                ] = {
                    "homepage":
                        "https://sb.koreainvestment.com/",
                    "isa_url":
                        KOREAINVEST_TARGETS[
                            "ISA"
                        ]["url"],
                    "irp_url":
                        KOREAINVEST_TARGETS[
                            "IRP"
                        ]["url"],
                    "isa_status":
                        "collector_error",
                    "irp_status":
                        "collector_error",
                    "error":
                        repr(e),
                    "updated_at":
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                }

                for category, output in (
                    ("ISA", isa_results),
                    ("IRP", irp_results),
                ):
                    output.append({
                        "bank": bank,
                        "category":
                            category,
                        "status":
                            "collector_error",
                        "source_url":
                            KOREAINVEST_TARGETS[
                                category
                            ]["url"],
                        "error":
                            repr(e),
                        "rates": {
                            f"{p}m": None
                            for p in TARGET_PERIODS
                        },
                        "updated_at":
                            datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                    })

            print()
            continue

        if not homepage:
            print(
                "  홈페이지 : latest_rates.json에서 미확인"
            )

            for kind, output in (
                ("isa", isa_results),
                ("irp", irp_results),
            ):
                output.append({
                    "bank": bank,
                    "category": kind.upper(),
                    "status": "homepage_not_found",
                    "rates": {
                        f"{p}m": None
                        for p in TARGET_PERIODS
                    },
                })

            print()
            continue

        print(
            "  홈페이지 :",
            homepage,
        )

        old = source_results.get(
            bank,
            {},
        )

        if not isinstance(
            old,
            dict,
        ):
            old = {}

        bank_source = {
            "homepage": homepage,
            "isa_url": old.get(
                "isa_url"
            ),
            "irp_url": old.get(
                "irp_url"
            ),
            "isa_status": old.get(
                "isa_status"
            ),
            "irp_status": old.get(
                "irp_status"
            ),
        }

        # ------------------------------------
        # ISA source
        # ------------------------------------

        isa_url = None

        if (
            old.get("isa_url")
            and old.get("isa_status")
            == "verified"
            and not is_homepage_only(
                old.get("isa_url"),
                homepage,
            )
        ):
            isa_url = old.get(
                "isa_url"
            )

            print(
                "  ISA URL : 기존 verified 재사용"
            )

        else:
            print(
                "  ISA URL : 집중 탐색 중..."
            )

            found = discover_source(
                bank,
                homepage,
                "isa",
            )

            if found:
                isa_url = found["url"]

                bank_source[
                    "isa_url"
                ] = isa_url

                bank_source[
                    "isa_status"
                ] = "discovered"

                bank_source[
                    "isa_score"
                ] = found["score"]

                print(
                    "           ",
                    isa_url,
                )

            else:
                print(
                    "            미확인"
                )

        # ------------------------------------
        # IRP source
        # ------------------------------------

        irp_url = None

        if (
            old.get("irp_url")
            and old.get("irp_status")
            == "verified"
            and not is_homepage_only(
                old.get("irp_url"),
                homepage,
            )
        ):
            irp_url = old.get(
                "irp_url"
            )

            print(
                "  IRP URL : 기존 verified 재사용"
            )

        else:
            print(
                "  IRP URL : 집중 탐색 중..."
            )

            found = discover_source(
                bank,
                homepage,
                "irp",
            )

            if found:
                irp_url = found["url"]

                bank_source[
                    "irp_url"
                ] = irp_url

                bank_source[
                    "irp_status"
                ] = "discovered"

                bank_source[
                    "irp_score"
                ] = found["score"]

                print(
                    "           ",
                    irp_url,
                )

            else:
                print(
                    "            미확인"
                )

        source_results[
            bank
        ] = bank_source

        # ------------------------------------
        # ISA rates
        # ------------------------------------

        if isa_url:
            isa_data = extract_rates_from_page(
                bank,
                "isa",
                isa_url,
            )
        else:
            isa_data = {
                "bank": bank,
                "category": "ISA",
                "status": "source_not_found",
                "source_url": None,
                "rates": {
                    f"{p}m": None
                    for p in TARGET_PERIODS
                },
            }

        isa_results.append(
            isa_data
        )

        print(
            "  ISA 금리 :",
            isa_data["rates"],
            f"[{isa_data['status']}]",
        )

        # ------------------------------------
        # IRP rates
        # ------------------------------------

        if irp_url:
            irp_data = extract_rates_from_page(
                bank,
                "irp",
                irp_url,
            )
        else:
            irp_data = {
                "bank": bank,
                "category": "IRP",
                "status": "source_not_found",
                "source_url": None,
                "rates": {
                    f"{p}m": None
                    for p in TARGET_PERIODS
                },
            }

        irp_results.append(
            irp_data
        )

        print(
            "  IRP 금리 :",
            irp_data["rates"],
            f"[{irp_data['status']}]",
        )

        print()

    # ----------------------------------------
    # SAVE
    # ----------------------------------------

    save_json(
        PENSION_SOURCES_FILE,
        source_results,
    )

    save_json(
        ISA_RATES_FILE,
        isa_results,
    )

    save_json(
        IRP_RATES_FILE,
        irp_results,
    )

    return (
        source_results,
        isa_results,
        irp_results,
    )


# ============================================
# SUMMARY
# ============================================

def print_summary(
    isa_results,
    irp_results,
):
    def count_status(
        rows,
        status,
    ):
        return sum(
            1
            for x in rows
            if x.get("status")
            == status
        )

    print("=" * 72)
    print(
        "수집 완료"
    )
    print("=" * 72)

    print(
        "ISA auto_extracted :",
        count_status(
            isa_results,
            "auto_extracted",
        ),
    )

    print(
        "ISA review_required:",
        count_status(
            isa_results,
            "review_required",
        ),
    )

    print(
        "IRP auto_extracted :",
        count_status(
            irp_results,
            "auto_extracted",
        ),
    )

    print(
        "IRP review_required:",
        count_status(
            irp_results,
            "review_required",
        ),
    )

    print()

    print(
        "ISA 저장:",
        ISA_RATES_FILE,
    )

    print(
        "IRP 저장:",
        IRP_RATES_FILE,
    )

    print(
        "URL 저장:",
        PENSION_SOURCES_FILE,
    )

    print()

    print(
        "※ auto_extracted = 3개 이상 기간 금리 자동확인"
    )

    print(
        "※ review_required = 1~2개 기간만 확인되어 수동검증 필요"
    )

    print(
        "※ rate_not_found = 페이지는 찾았으나 현재 정규식으로 금리표를 읽지 못함"
    )


# ============================================
# MAIN
# ============================================

def main():
    try:
        (
            source_results,
            isa_results,
            irp_results,
        ) = collect()

        print_summary(
            isa_results,
            irp_results,
        )

    except Exception as e:
        print()
        print(
            "[ERROR]"
        )
        print(
            str(e)
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
