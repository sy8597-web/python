from bs4 import BeautifulSoup
import requests
from datetime import datetime

# BeautifulSoup으로 네이버 검색 결과 크롤링하는 코드

# 1. 요청 헤더 설정 (네이버 차단 방지)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def crawl_naver_search(keyword, display_num=10):
    """
    네이버 검색 결과를 크롤링하는 함수
    
    Args:
        keyword: 검색 키워드
        display_num: 조회할 결과 개수 (기본값: 10)
    
    Returns:
        크롤링된 결과 리스트
    """
    
    # 네이버 검색 URL (모든 항목)
    url = f"https://search.naver.com/search.naver?query={keyword}&where=nexearch"
    
    try:
        # HTTP 요청
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        # BeautifulSoup으로 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 검색 결과 항목 찾기
        results = []
        
        # 클래스 기반 항목 추출
        items = soup.find_all('div', class_='fds-comps-right-image-text-container')
        
        for idx, item in enumerate(items[:display_num]):
            try:
                # 제목 추출
                title_elem = item.find('a', class_='fds-comps-right-image-text-title')
                title = title_elem.get_text(strip=True) if title_elem else 'N/A'
                
                # 링크 추출
                link = title_elem.get('href') if title_elem else 'N/A'
                
                # 내용 추출
                content_elem = item.find('a', class_='fds-comps-right-image-text-content')
                content = content_elem.get_text(strip=True) if content_elem else 'N/A'
                
                # 출처 정보 추출 (상위 구조에서)
                parent = item.find_parent('div', class_='fds-ugc-block-mod')
                if parent:
                    source_elem = parent.find('a', class_='fds-info-inner-text')
                    source = source_elem.get_text(strip=True) if source_elem else 'N/A'
                    
                    # 날짜 추출
                    date_elem = parent.find('span', class_='fds-info-sub-inner-text')
                    date = date_elem.get_text(strip=True) if date_elem else 'N/A'
                else:
                    source = 'N/A'
                    date = 'N/A'
                
                result = {
                    'no': idx + 1,
                    'title': title,
                    'source': source,
                    'date': date,
                    'content': content[:100] + '...' if len(content) > 100 else content,
                    'link': link
                }
                
                results.append(result)
                
            except Exception as e:
                print(f"항목 {idx + 1} 파싱 오류: {e}")
                continue
        
        return results
    
    except requests.exceptions.RequestException as e:
        print(f"요청 오류: {e}")
        return []
    except Exception as e:
        print(f"오류 발생: {e}")
        return []


def print_results(results):
    """크롤링 결과를 보기 좋게 출력"""
    
    if not results:
        print("검색 결과가 없습니다.")
        return
    
    print("\n" + "="*100)
    print("네이버 검색 결과")
    print("="*100 + "\n")
    
    for result in results:
        print(f"[{result['no']}] {result['title']}")
        print(f"출처: {result['source']}")
        print(f"날짜: {result['date']}")
        print(f"내용: {result['content']}")
        print(f"링크: {result['link']}")
        print("-" * 100 + "\n")


def save_to_file(results, filename='naver_search_result.txt'):
    """크롤링 결과를 파일로 저장"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("="*100 + "\n")
        f.write(f"네이버 검색 결과 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
        f.write("="*100 + "\n\n")
        
        for result in results:
            f.write(f"[{result['no']}] {result['title']}\n")
            f.write(f"출처: {result['source']}\n")
            f.write(f"날짜: {result['date']}\n")
            f.write(f"내용: {result['content']}\n")
            f.write(f"링크: {result['link']}\n")
            f.write("-" * 100 + "\n\n")
    
    print(f"✓ 결과가 '{filename}' 파일로 저장되었습니다.")


# ============ 사용 예제 ============

if __name__ == "__main__":
    # 검색 키워드 설정
    keyword = "아이폰17"
    
    print(f"'{keyword}' 검색 중...")
    
    # 크롤링 실행
    results = crawl_naver_search(keyword, display_num=10)
    
    # 결과 출력
    print_results(results)
    
    # 파일로 저장
    if results:
        save_to_file(results)
