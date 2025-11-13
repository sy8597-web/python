# kimpga_top20.py (김프 크롤러)
import argparse
import re
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional

URL = "https://kimpga.com/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch_html(url: str, timeout: int = 15) -> Optional[str]:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"[fetch_html] 요청 실패: {e}")
        return None


def fetch_with_selenium(url: str, wait: int = 3) -> Optional[str]:
    """Selenium을 사용해 렌더된 HTML을 가져옵니다. webdriver-manager를 사용합니다.
    이 함수는 Selenium 또는 webdriver-manager가 설치되어 있지 않으면 None을 반환합니다n"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
    except Exception as e:
        print(f"[fetch_with_selenium] Selenium 또는 webdriver-manager import 실패: {e}")
        return None

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        # 간단한 대기: JS가 로드될 시간을 줌
        import time

        time.sleep(wait)
        html = driver.page_source
        driver.quit()
        return html
    except Exception as e:
        print(f"[fetch_with_selenium] 실행 실패: {e}")
        try:
            driver.quit()
        except Exception:
            pass
        return None


def parse_number(s: str) -> Optional[float]:
    if not s:
        return None
    s = s.strip()
    # 콤마, 통화기호 등 비숫자 문자 제거
    s = re.sub(r"[^0-9.\-]", "", s.replace(",", ""))
    try:
        return float(s)
    except Exception:
        return None


def parse_top_coins(html: str, top_n: int = 20) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    results: List[Dict] = []

    # 1) 테이블 기반 탐색: 가장 많은 tr을 가진 table 사용
    tables = soup.find_all("table")
    candidate = None
    max_tr = 0
    for t in tables:
        tr_count = len(t.find_all("tr"))
        if tr_count > max_tr:
            max_tr = tr_count
            candidate = t

    if candidate and max_tr >= 5:
        rows = candidate.find_all("tr")
        for r in rows:
            cols = [td.get_text(strip=True) for td in r.find_all(["td", "th"])]
            if not cols or len(cols) < 2:
                continue
            name = cols[0]
            price = parse_number(cols[1]) if len(cols) >= 2 else None
            extra = cols[2:] if len(cols) > 2 else []
            results.append({"name": name, "price": price, "extra": extra})
            if len(results) >= top_n:
                break

    # 2) 카드/리스트 기반 탐색
    if not results:
        selectors = [
            "div.coin",
            "div.ticker",
            "li.coin",
            "ul.coin-list li",
            "div.currency",
            "div.market-row",
            "div.coin-row",
            "div.table-row",
        ]
        items = []
        for sel in selectors:
            found = soup.select(sel)
            if found and len(found) > 0:
                items = found
                break

        if not items:
            candidates = []
            for tag in soup.find_all(True):
                text = tag.get_text(" ", strip=True)
                if re.search(r"\d{1,3}(?:[,\d]{0,}\d)?(?:\.\d+)?", text):
                    candidates.append(tag)
            items = candidates

        for it in items:
            text = it.get_text(" ", strip=True)
            parts = [p for p in re.split(r"\s{2,}|\s*\|\s*|\n", text) if p]
            if not parts:
                continue
            name = parts[0]
            price = None
            for p in parts[1:]:
                val = parse_number(p)
                if val is not None:
                    price = val
                    break
            results.append({"name": name, "price": price, "extra_text": " | ".join(parts[1:])})
            if len(results) >= top_n:
                break

    filtered = [r for r in results if r.get("name")]
    return filtered[:top_n]


def save_csv(items: List[Dict], filename: str):
    if not items:
        print("[save_csv] 저장할 항목이 없습니다.")
        return
    keys = set()
    for it in items:
        keys.update(it.keys())
    keys = ["name", "price"] + sorted(k for k in keys if k not in ("name", "price"))
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for it in items:
            writer.writerow(it)
    print(f"[save_csv] 저장 완료: {filename}")


def main():
    parser = argparse.ArgumentParser(description="kimpga 상위 코인 크롤러")
    parser.add_argument("--selenium", action="store_true", help="Selenium으로 렌더링된 페이지를 사용")
    parser.add_argument("--top", type=int, default=20, help="추출할 상위 개수")
    parser.add_argument("--wait", type=int, default=3, help="Selenium 대기 시간(초)")
    args = parser.parse_args()

    print("kimpga 크롤러 시작:", URL)
    html = fetch_html(URL)
    if (not html or len(html) < 100) and args.selenium:
        print("정적 요청으로 충분치 않아 Selenium으로 재시도합니다...")
        html = fetch_with_selenium(URL, wait=args.wait)

    if not html:
        # 마지막 시도: Selenium 자동 시도
        print("정적 요청으로 HTML을 가져오지 못했습니다. Selenium으로 시도합니다...")
        html = fetch_with_selenium(URL, wait=args.wait)

    if not html:
        print("페이지를 가져오지 못했습니다. 네트워크/방화벽 또는 사이트 차단을 확인하세요.")
        return

    items = parse_top_coins(html, top_n=args.top)
    if not items:
        print("파싱된 항목이 없습니다. 페이지 구조가 동적이거나 선택자가 맞지 않습니다.")
        return

    print(f"파싱된 항목 수: {len(items)}")
    for i, it in enumerate(items, 1):
        print(f"{i:02d}. {it.get('name')[:80]} - price: {it.get('price')} - extra: {it.get('extra', it.get('extra_text',''))}")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"kimpga_top{args.top}_{ts}.csv"
    save_csv(items, filename)


if __name__ == "__main__":
    main()