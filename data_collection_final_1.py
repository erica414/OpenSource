import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  # TimeoutException을 import

# 국밥집 리뷰창 URL(입력받음)
url = input("데이터를 수집할 국밥집(리뷰창) url : ")
# 웹드라이버 실행
wd = webdriver.Chrome()
wd.get(url)
time.sleep(2)

# 정렬버튼 클릭 -> 최신순
address = "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde > div.m6QErb.Pf6ghf.XiKgde.KoSBEe.ecceSd.tLjsW > div.TrU0dc.kdfrQc.NUqjXc > button"
wd.find_element(By.CSS_SELECTOR, address).click()
time.sleep(2)

address1 = "#action-menu > div > div:nth-child(2)"
wd.find_element(By.CSS_SELECTOR, address1).click()
time.sleep(2)

scrollable_div = wd.find_element(By.CSS_SELECTOR,
    "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde")
time.sleep(2)

#리뷰 하나당 개수를 세기 위한 클래스 이름
review_selector = "div.jJc9Ad"

# 수집할 리뷰 개수 설정
total_review_count = 3000  # 목표 리뷰 수

# 스크롤 전, 현재 로드된 리뷰 개수 확인
# find_element's'를 사용해서 클래스 이름과 일치한 요소를 찾고 리스트에 담아줌. 이 리스트의 개수를 계속 비교
last_review_count = len(wd.find_elements(By.CSS_SELECTOR, review_selector))
print(f"스크롤 시작 전 리뷰 개수: {last_review_count}")

# 안정 종료 카운터
stable_count = 0
STABLE_LIMIT = 10  # 10회 연속 증가 없으면 종료

# 스크롤 반복문
while True:
    try:
        current_review_count = len(wd.find_elements(By.CSS_SELECTOR, review_selector))
        print(f"현재까지 로드된 리뷰 개수: {current_review_count}")

        # 목표 리뷰 개수 이상이면 종료
        if current_review_count >= total_review_count:
            print(f"목표 리뷰 개수({total_review_count}개) 이상 로드됨 → 스크롤 종료")
            break

        # 10회 연속 변화 없음 → 자동 종료
        if current_review_count == last_review_count:
            stable_count += 1
        else:
            stable_count = 0

        if stable_count >= STABLE_LIMIT:
            print(f"리뷰 개수 증가 없음 ({STABLE_LIMIT}회 연속) → 스크롤 종료")
            break

        # 스크롤 실행
        scrollable_div.send_keys(Keys.END)
        time.sleep(2)

        # 기준값 갱신
        last_review_count = current_review_count

    except Exception as e:
        print(f"스크롤 중 오류 발생: {e}")
        break

html = wd.page_source
bs_obj = BeautifulSoup(html, "html.parser")
div = bs_obj.find("div", {"class": "m6QErb XiKgde"})
reviews = div.findAll("div", {"class": "jftiEf fontBodyMedium"})

# 브라우저 종료
wd.quit()


# 데이터프레임으로 변환
data1 = []
col = ['작성자', '날짜', '평점', '리뷰']

for i in reviews:
    try:
        ID = i.find("div", {"class":"d4r55"})
        Date = i.find("span", {"class":"rsqaWe"})
        r_temp = i.find("span", {"class":"kvMYJc"})
        r = r_temp["aria-label"]
        contents = i.find("span", {"class":"wiI7pd"})
        contents_text = contents.text if contents else None #값 있을 때, 없을 때
        row = [ID.text, Date.text, r, contents_text]
        data1.append(row)
    except:
        continue

df = pd.DataFrame(data1, columns=col)

# 폴더 경로 입력
path = input("저장할 폴더 경로를 입력하세요 (예: C:/홍길동/오픈소스소프트웨어): ").strip()
# 파일 이름 입력
file_name = input("저장할 파일 이름을 입력하세요 (예: test_porksoup_google_review): ").strip()

# 확장자 및 경로 결합
if not file_name.endswith(".csv"):
    file_name += ".csv"
path_filename = path + "/" + file_name

# 데이터프레임을 파일에 저장 -> 저장할 파일 주소 + 파일 이름 작성
df.to_csv(path_filename, encoding = "utf-8-sig", index = False)