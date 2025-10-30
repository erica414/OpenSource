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
import re  # 숫자 추출용

url = 'https://www.google.com/maps/place/%EC%88%98%EB%9D%BC%EB%8F%BC%EC%A7%80%EA%B5%AD%EB%B0%A5/data=!4m8!3m7!1s0x3568ecf12202becd:0x58eb4205927036a6!8m2!3d35.1360893!4d129.0993841!9m1!1b1!16s%2Fg%2F11bwymmvb8?entry=ttu&g_ep=EgoyMDI1MTAyOC4wIKXMDSoASAFQAw%3D%3D'
wd = webdriver.Chrome()
wd.get(url)
time.sleep(2)

# 정렬 버튼 클릭
address = "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde > div.m6QErb.Pf6ghf.XiKgde.KoSBEe.ecceSd.tLjsW > div.TrU0dc.kdfrQc.NUqjXc > button"
wd.find_element(By.CSS_SELECTOR, address).click()
time.sleep(2)

# 최신순으로 변경
address1 = "#action-menu > div > div:nth-child(2)"
wd.find_element(By.CSS_SELECTOR, address1).click()
time.sleep(2)

# 스크롤 할 영역 선택 
scrollable_div = wd.find_element(By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde")
time.sleep(2)

# 전체 리뷰 수 파싱
# 1차: 장소 헤더 구조(F7nice), 2차: 리뷰 패널 내부(RWgCYc)
total_text = None
try:
    total_text = wd.find_element(By.CSS_SELECTOR, "div.F7nice span[aria-label]").get_attribute("aria-label")
except Exception:
    try:
        total_text = wd.find_element(By.CSS_SELECTOR, "div.m6QErb span.RWgCYc").text
    except Exception as e:
        # 전체 리뷰 수 파싱 실패
        total_number = None

if total_text:
    try:
        total_number = int(re.sub(r'[^0-9]', '', total_text))
        #print(f"전체 리뷰 수 감지: {total_number}개")
    except Exception as e:
        # 숫자 변환 실패
        total_number = None
else:
    total_number = None

# 사용자 입력 값 받기. 없거나 잘못되면 None
try:
    user_input = input("크롤링할 리뷰 개수를 입력하세요 (Enter 시 전체 수집/자동정지 사용): ")
    user_count = int(user_input) if user_input.strip() != "" else None
except ValueError:
    # 유효하지 않은 입력값이면 무한 크롤링 -> 10회 이상 같은 값 유지 시 종료
    user_count = None

# 목표치 기반 종료를 사용할지, 안정 종료만 사용할지 결정
use_target_threshold = False
if (total_number is not None) or (user_count is not None):
    # 둘 중 하나라도 있으면 목표치 기반 종료를 활성화
    if total_number is None:
        target_review_count = user_count
    elif user_count is None:
        target_review_count = total_number
    else:
        target_review_count = min(total_number, user_count)
    use_target_threshold = True
    print(f"수집 목표 리뷰 수: {target_review_count}개")
else:
    # 둘 다 없으면 기본값 지정하지 않고 '안정 종료(연속 동일 개수 10회)'만 사용
    target_review_count = None

#리뷰 하나당 개수를 세기 위한 클래스 이름
review_selector = "div.jJc9Ad"

# 스크롤 전, 현재 로드된 리뷰 개수 확인
last_review_count = len(wd.find_elements(By.CSS_SELECTOR, review_selector))
print(f"스크롤 시작 전 리뷰 개수: {last_review_count}")

# 안정 종료 카운터
stable_count = 0
STABLE_LIMIT = 10  # 네트워크 지연 고려하여 여유있게 10회

#반복문
while True:
    try:
        current_review_count = len(wd.find_elements(By.CSS_SELECTOR, review_selector))
        print(f"현재까지 로드된 리뷰 개수: {current_review_count}")
        
        # (옵션) 목표 개수 도달 시 종료
        if use_target_threshold and (current_review_count >= target_review_count):
            print(f"목표 리뷰 개수({target_review_count}개) 이상을 로드하여 스크롤을 종료합니다.")
            break

        # 안정 종료 체크: 연속 10회 증가 없음 → 종료
        if current_review_count == last_review_count:
            stable_count += 1
        else:
            stable_count = 0

        if stable_count >= STABLE_LIMIT:
            print(f"리뷰 개수 증가 없음 ({STABLE_LIMIT}회 연속) → 스크롤 종료")
            break
        
        # 스크롤
        scrollable_div.send_keys(Keys.END)
        time.sleep(2)
        
        # 기준 업데이트
        last_review_count = current_review_count
        
    except Exception as e:  # as e는 오류의 내용을 변수에 저장하는 코드
        print(f"스크롤 중 오류 발생: {e}")
        break

html = wd.page_source
bs_obj = BeautifulSoup(html, "html.parser")
div = bs_obj.find("div", {"class" : "m6QErb XiKgde"}) 
reviews = div.findAll("div", {"class":"jftiEf fontBodyMedium"})

wd.quit()

# 수집한 데이터를 데이터프레임 형태로 변환
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