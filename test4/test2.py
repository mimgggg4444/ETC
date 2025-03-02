from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 크롬 드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 브라우저 창 없이 실행

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 웹사이트 접속
url = "https://example.com"
driver.get(url)

# HTML 소스코드 가져오기
html = driver.page_source
print("📌 HTML 코드:")
print(html)

# CSS 파일 가져오기
css_links = driver.find_elements("css selector", "link[rel='stylesheet']")
for link in css_links:
    href = link.get_attribute("href")
    if href:
        driver.get(href)
        print(f"\n📌 CSS 파일 ({href}):")
        print(driver.page_source)

driver.quit()