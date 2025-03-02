import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 타겟 URL
url = "https://accounts.kakao.com/login/?continue=https%3A%2F%2Faccounts.kakao.com%2Fweblogin%2Faccount#webTalkLogin"

# 적절한 헤더 설정 (User-Agent 지정)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

# HTML 컨텐츠 가져오기
response = requests.get(url, headers=headers)
html_content = response.text

# HTML 출력 또는 파일 저장 등 처리
print("HTML Content:")
print(html_content)

# BeautifulSoup를 이용하여 HTML 파싱
soup = BeautifulSoup(html_content, "html.parser")

# rel="stylesheet"인 <link> 태그에서 CSS 파일 URL 추출
css_links = []
for link in soup.find_all("link", rel="stylesheet"):
    href = link.get("href")
    if href:
        full_url = urljoin(url, href)
        css_links.append(full_url)

# 추출한 CSS 링크들을 이용하여 CSS 컨텐츠 가져오기
for css_url in css_links:
    css_response = requests.get(css_url, headers=headers)
    if css_response.status_code == 200:
        css_content = css_response.text
        print(f"\nCSS from {css_url}:")
        print(css_content)
    else:
        print(f"\nFailed to retrieve CSS from {css_url}")