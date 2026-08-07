# -*- coding: utf-8 -*-
"""
SBRateBot V5 - 한국투자저축은행 ISA / 퇴직연금 금리 실수집기

수집 대상
- ISA정기예금: PRD-PDS001-10
- 퇴직연금정기예금: PRD-PDS001-11

수집 방식
- Selenium + 실제 Edge/Chrome 렌더링 DOM
- 금리안내 영역: #mf_wfm_contents_intrGridView
- 한국투자 WebSquare 화면이 렌더링한 실제 금리표를 읽음

출력
- data/koreainvest_rates.json

실행
    cd C:\\SBRateBot_V5
    py crawler\\koreainvest.py

필요 패키지
    pip install selenium
"""

import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path


# ============================================================
# 기본 설정
# ============================================================

BANK_NAME = "한국투자저축은행"

TARGETS = {
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

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUT_JSON = DATA_DIR / "koreainvest_rates.json"

WAIT_TIMEOUT = 30


# ============================================================
# 공통 유틸
# ============================================================

def clean_text(value):
    if value is None:
        return ""

    value = str(value)
    value = value.replace("\xa0", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def parse_rate(value):
    """
    '3.75%', ' 3.75 ', '연 3.75%' 등을 float 3.75로 변환.
    """
    text = clean_text(value)

    match = re.search(r"(\d+(?:\.\d+)?)", text)
    if not match:
        return None

    try:
        return float(match.group(1))
    except ValueError:
        return None


def normalize_period(value):
    """
    '3개월', '12 개월' 등을 '3개월', '12개월'로 정규화.
    """
    text = clean_text(value)

    match = re.search(r"(\d+)\s*개월", text)
    if not match:
        return text

    return f"{int(match.group(1))}개월"


def parse_reference_date(text):
    """
    예:
    2026년 08월 03일
    2026년 08월 01일 기준
    """
    text = clean_text(text)

    match = re.search(
        r"(\d{4})\s*년\s*(\d{1,2})\s*월\s*(\d{1,2})\s*일",
        text,
    )

    if not match:
        return None

    year, month, day = map(int, match.groups())

    return f"{year:04d}-{month:02d}-{day:02d}"


def month_key(value):
    """
    '2026.08' -> (2026, 8)
    """
    text = clean_text(value)

    match = re.search(r"(\d{4})\D+(\d{1,2})", text)
    if not match:
        return (0, 0)

    return (
        int(match.group(1)),
        int(match.group(2)),
    )


# ============================================================
# Selenium Driver
# ============================================================

def create_driver():
    """
    회사 PC에서 확인된 Microsoft Edge를 우선 사용.
    실패하면 Chrome으로 자동 전환.
    """

    edge_error = None

    try:
        from selenium import webdriver
        from selenium.webdriver.edge.options import Options as EdgeOptions

        options = EdgeOptions()

        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1600,1200")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")

        print("[DRIVER] Microsoft Edge 시도")

        driver = webdriver.Edge(
            options=options
        )

        driver.set_page_load_timeout(
            WAIT_TIMEOUT
        )

        return driver, "Edge"

    except Exception as e:
        edge_error = e

        print(
            "[DRIVER] Edge 실패:",
            repr(e)
        )

    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options as ChromeOptions

        options = ChromeOptions()

        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1600,1200")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")

        print("[DRIVER] Google Chrome 시도")

        driver = webdriver.Chrome(
            options=options
        )

        driver.set_page_load_timeout(
            WAIT_TIMEOUT
        )

        return driver, "Chrome"

    except Exception as chrome_error:
        raise RuntimeError(
            "Edge / Chrome WebDriver 실행 실패\n"
            f"Edge: {repr(edge_error)}\n"
            f"Chrome: {repr(chrome_error)}"
        )


# ============================================================
# 페이지 로딩
# ============================================================

def wait_for_product_page(
    driver,
    expected_title,
):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    wait = WebDriverWait(
        driver,
        WAIT_TIMEOUT,
    )

    # 금리 영역 렌더링 대기
    wait.until(
        EC.presence_of_element_located(
            (
                By.ID,
                "mf_wfm_contents_intrGridView",
            )
        )
    )

    # 상품명이 들어올 때까지 추가 확인
    wait.until(
        lambda d:
            expected_title in clean_text(d.title)
            or expected_title in clean_text(
                d.find_element(
                    By.TAG_NAME,
                    "body"
                ).text
            )
    )

    # WebSquare DOM 안정화
    time.sleep(2)


def get_rate_section(driver):
    """
    금리안내 영역을 브라우저 DOM에서 구조화하여 반환.
    """
    script = r"""
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

    const tableData =
        tables.map((table, tableIndex) => {

            const rows =
                Array.from(
                    table.querySelectorAll("tr")
                ).map(row => {

                    return Array.from(
                        row.querySelectorAll(
                            "th, td"
                        )
                    ).map(cell => ({

                        text:
                            (cell.innerText || "")
                            .replace(/\s+/g, " ")
                            .trim(),

                        tag:
                            cell.tagName,

                        rowspan:
                            cell.getAttribute(
                                "rowspan"
                            ) || "1",

                        colspan:
                            cell.getAttribute(
                                "colspan"
                            ) || "1"

                    }));

                });

            return {
                tableIndex,
                rows
            };

        });

    return {

        text:
            (root.innerText || "")
            .replace(/\s+/g, " ")
            .trim(),

        html:
            root.innerHTML,

        tables:
            tableData

    };
    """

    return driver.execute_script(
        script
    )


# ============================================================
# ISA 파싱
# ============================================================

def parse_isa(section):
    if not section:
        raise ValueError(
            "ISA 금리안내 영역을 찾지 못했습니다."
        )

    reference_date = parse_reference_date(
        section.get("text", "")
    )

    rates = []

    for table in section.get(
        "tables",
        []
    ):

        rows = table.get(
            "rows",
            []
        )

        for row in rows:
            texts = [
                clean_text(
                    cell.get("text")
                )
                for cell in row
            ]

            if len(texts) < 2:
                continue

            period = normalize_period(
                texts[0]
            )

            if not re.fullmatch(
                r"\d+개월",
                period
            ):
                continue

            rate = parse_rate(
                texts[1]
            )

            if rate is None:
                continue

            rates.append({
                "period": period,
                "rate": rate,
                "rate_type": "ISA",
            })

        # 첫 번째 정상 기간별 금리표만 사용
        if rates:
            break

    if not rates:
        raise ValueError(
            "ISA 기간별 금리를 추출하지 못했습니다."
        )

    rates.sort(
        key=lambda x:
            int(
                x["period"].replace(
                    "개월",
                    ""
                )
            )
    )

    return {
        "product_name": "ISA정기예금",
        "reference_date": reference_date,
        "rates": rates,
    }


# ============================================================
# IRP 파싱
# ============================================================

def parse_irp(section):
    if not section:
        raise ValueError(
            "IRP 금리안내 영역을 찾지 못했습니다."
        )

    reference_date = parse_reference_date(
        section.get("text", "")
    )

    target_rows = []

    # DC/IRP형, DB형 헤더가 있는 테이블 선택
    for table in section.get(
        "tables",
        []
    ):

        rows = table.get(
            "rows",
            []
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
            and
            "DB형" in joined
        ):
            target_rows = rows
            break

    if not target_rows:
        raise ValueError(
            "IRP 금리 테이블을 찾지 못했습니다."
        )

    # period별 월별 데이터 수집
    period_month_rows = {}

    current_period = None

    for row in target_rows:

        # th-only 헤더 제외
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

        first_period = normalize_period(
            texts[0]
        )

        # rowspan 첫 행:
        # 3개월 | 2026.07 | 2.00 | 2.00
        if re.fullmatch(
            r"\d+개월",
            first_period
        ):
            current_period = first_period

            if len(texts) < 4:
                continue

            rate_month = texts[1]
            dc_irp = parse_rate(
                texts[2]
            )
            db = parse_rate(
                texts[3]
            )

        else:
            # rowspan 후속 행:
            # 2026.08 | 2.00 | 2.00
            if current_period is None:
                continue

            if len(texts) < 3:
                continue

            rate_month = texts[0]
            dc_irp = parse_rate(
                texts[1]
            )
            db = parse_rate(
                texts[2]
            )

        if (
            dc_irp is None
            and
            db is None
        ):
            continue

        period_month_rows.setdefault(
            current_period,
            []
        ).append({
            "rate_month": clean_text(
                rate_month
            ),
            "dc_irp_rate": dc_irp,
            "db_rate": db,
        })

    if not period_month_rows:
        raise ValueError(
            "IRP 기간별 금리를 추출하지 못했습니다."
        )

    # 각 기간별 가장 최신 월 사용
    rates = []

    for period, monthly_rows in (
        period_month_rows.items()
    ):

        latest = max(
            monthly_rows,
            key=lambda x:
                month_key(
                    x["rate_month"]
                )
        )

        rates.append({
            "period": period,
            "rate_month":
                latest["rate_month"],
            "dc_irp_rate":
                latest["dc_irp_rate"],
            "db_rate":
                latest["db_rate"],
        })

    rates.sort(
        key=lambda x:
            int(
                x["period"].replace(
                    "개월",
                    ""
                )
            )
    )

    return {
        "product_name":
            "퇴직연금정기예금",
        "reference_date":
            reference_date,
        "rates":
            rates,
    }


# ============================================================
# 상품 수집
# ============================================================

def collect_product(
    driver,
    kind,
    config,
):
    print()
    print(
        "=" * 92
    )
    print(
        f"[{kind}] {config['url']}"
    )
    print(
        "=" * 92
    )

    driver.get(
        config["url"]
    )

    wait_for_product_page(
        driver,
        config["expected_title"],
    )

    print(
        "[TITLE]",
        driver.title
    )

    section = get_rate_section(
        driver
    )

    if kind == "ISA":
        parsed = parse_isa(
            section
        )

    elif kind == "IRP":
        parsed = parse_irp(
            section
        )

    else:
        raise ValueError(
            f"지원하지 않는 유형: {kind}"
        )

    parsed.update({
        "type": kind,
        "menu_id":
            config["menu_id"],
        "source_url":
            config["url"],
    })

    return parsed


# ============================================================
# 출력
# ============================================================

def print_result(result):
    print()
    print(
        f"[{result['type']}] "
        f"{result['product_name']}"
    )

    print(
        "기준일:",
        result.get(
            "reference_date"
        )
    )

    if result["type"] == "ISA":

        for row in result[
            "rates"
        ]:

            print(
                f"  {row['period']:>5} "
                f": {row['rate']:.2f}%"
            )

    else:

        for row in result[
            "rates"
        ]:

            dc = row.get(
                "dc_irp_rate"
            )

            db = row.get(
                "db_rate"
            )

            dc_text = (
                f"{dc:.2f}%"
                if dc is not None
                else "-"
            )

            db_text = (
                f"{db:.2f}%"
                if db is not None
                else "-"
            )

            print(
                f"  {row['period']:>5} "
                f"[{row['rate_month']}] "
                f"DC/IRP {dc_text} "
                f"/ DB {db_text}"
            )


# ============================================================
# Main
# ============================================================

def main():
    print(
        "=" * 92
    )
    print(
        "SBRateBot V5 - "
        "한국투자저축은행 ISA / IRP "
        "금리 실수집"
    )
    print(
        "=" * 92
    )

    try:
        import selenium  # noqa: F401
    except ImportError:
        print()
        print(
            "[ERROR] selenium이 없습니다."
        )
        print(
            "pip install selenium"
        )
        sys.exit(1)

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    driver = None

    try:
        driver, browser_name = (
            create_driver()
        )

        products = {}

        for kind, config in (
            TARGETS.items()
        ):
            result = collect_product(
                driver,
                kind,
                config,
            )

            products[kind] = result

            print_result(
                result
            )

        output = {
            "bank": BANK_NAME,
            "browser":
                browser_name,
            "collected_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            "products":
                products,
        }

        OUT_JSON.write_text(
            json.dumps(
                output,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        print()
        print(
            "=" * 92
        )
        print(
            "수집 완료"
        )
        print(
            "=" * 92
        )
        print(
            "저장:",
            OUT_JSON
        )

    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass


if __name__ == "__main__":
    main()
