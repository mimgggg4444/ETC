import requests
from bs4 import BeautifulSoup

# 크롤링할 웹사이트 URL
url = "https://example.com"  # 원하는 웹사이트로 변경

# 웹페이지 요청
response = requests.get(url)

# HTML 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# HTML 코드 출력
print("📌 HTML 코드:")
print(soup.prettify())

# CSS 파일 링크 찾기
css_links = [link['href'] for link in soup.find_all('link', rel='stylesheet') if 'href' in link.attrs]

# CSS 파일 가져오기
for css_link in css_links:
    if css_link.startswith('/'):  # 상대 경로라면 절대 URL로 변경
        css_link = url + css_link
    css_response = requests.get(css_link)
    print(f"\n📌 CSS 파일 ({css_link}):")
    print(css_response.text)