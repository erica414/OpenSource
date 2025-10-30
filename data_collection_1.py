import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

url = 'https://www.google.com/maps/place/60%EB%85%84%EC%A0%84%ED%86%B5+%ED%95%A0%EB%A7%A4%EA%B5%AD%EB%B0%A5/data=!4m8!3m7!1s0x3568eb9be8234d39:0x55451c7ce805a0d2!8m2!3d35.1410105!4d129.0561679!9m1!1b1!16s%2Fg%2F1hm5614rq?entry=ttu&g_ep=EgoyMDI1MDkyOS4wIKXMDSoASAFQAw%3D%3D'
wd = webdriver.Chrome()
wd.get(url)
time.sleep(2)

address = "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde > div.m6QErb.Pf6ghf.XiKgde.KoSBEe.ecceSd.tLjsW > div.TrU0dc.kdfrQc.NUqjXc > button"
wd.find_element(By.CSS_SELECTOR, address).click()
time.sleep(2)

address1 = "#action-menu > div > div:nth-child(2)"
wd.find_element(By.CSS_SELECTOR, address1).click()
time.sleep(2)

scrollable_div = wd.find_element(By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde")
time.sleep(2)

# for i in range(3000):
#     try: 
#         scrollable_div.send_keys(Keys.END) 
#         time.sleep(1)
#     except: 
#         continue
last_height = 0
while True:
    try:
        scrollable_div.send_keys(Keys.END)
        time.sleep(1)
        # 현재 스크롤 영역의 높이 확인
        current_height = wd.execute_script("return arguments[0].scrollHeight", scrollable_div)
        if current_height == last_height:  # 더 이상 로딩될 내용 없음
            break
        last_height = current_height
    except:
        break
    
html = wd.page_source
bs_obj = BeautifulSoup(html, "html.parser")
div = bs_obj.find("div", {"class" : "m6QErb XiKgde"}) 
reviews = div.findAll("div", {"class":"jftiEf fontBodyMedium"})

print(reviews)

for i in reviews:
     try:
         ID = i.find("div", {"class":"d4r55"})
         Date = i.find("span", {"class":"rsqaWe"})
         r_temp = i.find("span", {"class":"kvMYJc"})
         r = r_temp["aria-label"]
         contents = i.find("span", {"class":"wiI7pd"})
         contents_text = contents.text if contents else None #값 있을 때, 없을 때
         row = [ID.text, Date.text, r, contents_text]
         data.append(row)
     except:
             continue
df = pd.DataFrame(data, columns=col)