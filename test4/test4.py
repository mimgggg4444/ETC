import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 다운로드 받을 웹사이트 URL
url = "https://accounts.kakao.com/login/?continue=https%3A%2F%2Faccounts.kakao.com%2Fweblogin%2Faccount#webTalkLogin"

# HTML 다운로드
response = requests.get(url)
html_content = response.text

# HTML 저장 (page.html)
with open("page.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# BeautifulSoup를 사용해 HTML 파싱
soup = BeautifulSoup(html_content, "html.parser")

# CSS 링크 추출 (rel="stylesheet"인 link 태그)
css_links = [link.get("href") for link in soup.find_all("link", rel="stylesheet")]

# CSS 파일을 저장할 폴더 생성
if not os.path.exists("css"):
    os.makedirs("css")

# 각 CSS 파일 다운로드
for css in css_links:
    # 상대경로인 경우 절대경로로 변환
    css_url = urljoin(url, css)
    try:
        css_response = requests.get(css_url)
        css_file_name = os.path.basename(css_url.split("?")[0])
        css_path = os.path.join("css", css_file_name)
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(css_response.text)
        print(f"다운로드 완료: {css_path}")
    except Exception as e:
        print(f"다운로드 실패 ({css_url}): {e}")