import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
url = "https://www.jobplanet.co.kr/job"
driver = webdriver.Chrome()
driver.implicitly_wait(3)
driver.get(url)
driver.find_element(By.CSS_SELECTOR,'button.jply_btn_sm.inner_text.jf_b2').click()
count = 0
def init():
    # 대기 시간을 10초로 설정하고, filter_depth1 클래스를 가진 요소가 나타날 때까지 대기
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'filter_depth1'))
    )
    # filter_depth1 클래스를 가진 요소 내에서 개발 버튼을 찾아 클릭
    development_button = element.find_element(By.XPATH, '//button[text()="개발"]')
    development_button.click()
    # 개발 버튼을 클릭한 후에 수행할 작업을 여기에 추가
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'filter_depth2'))
    )
    development_button = element.find_element(By.XPATH, '//label[contains(.//span, "개발 전체")]')
    development_button.click()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'panel_bottom'))
    )
    # panel_bottom 클래스를 가진 요소 내에서 "적용" 버튼을 찾아 클릭
    apply_button = element.find_element(By.XPATH, '//button[text()="적용"]')
    apply_button.click()
    time.sleep(2)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'recruitment-content'))
    )
    main_window_handle = driver.current_window_handle
    # recruitment-content 클래스를 가진 요소 내에서 첫 번째 링크를 다시 찾아서 클릭
    # 첫 번째 링크 클릭
    first_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.recruitment-content .item-card a'))
    )
    first_link_url = first_link.get_attribute("href")
    first_link.click()

    # 모든 창 핸들 확인
    all_window_handles = driver.window_handles

    # 새로 열린 창의 핸들 찾기
    new_window_handle = [handle for handle in all_window_handles if handle != main_window_handle][0]

    # 새로 열린 창으로 전환
    driver.switch_to.window(new_window_handle)

    driver.get(first_link_url)

def summary():
    data = []
    company_name= driver.find_element(By.CSS_SELECTOR,'.company_name a').text.strip()
    deadline = driver.find_element(By.CSS_SELECTOR,'.calendar .cont .day_text').text.strip()
    job_title = driver.find_element(By.CSS_SELECTOR,'.briefcase .cont span').text.strip()
    experience = driver.find_element(By.CSS_SELECTOR,'.experience .cont span').text.strip()
    employment_type = driver.find_element(By.CSS_SELECTOR,'.type .cont').text.strip()
    salary = driver.find_element(By.CSS_SELECTOR,'.money .cont span').text.strip()
    skills = driver.find_element(By.CSS_SELECTOR,'.skill .cont').text.strip()

    try:
        intro_element = driver.find_element(By.XPATH,"//*[text()='기업소개']/following-sibling::div").text.strip()
    except NoSuchElementException:
        intro_element = "기업소개 정보를 찾을 수 없습니다."
    try:
        job_duties = driver.find_element(By.XPATH,"//*[text()='주요업무']/following-sibling::div").text.strip()
    except NoSuchElementException:
        job_duties = "주요업무 정보를 찾을 수 없습니다."
    try:
        qual = driver.find_element(By.XPATH,"//*[text()='자격요건']/following-sibling::div").text.strip()
    except NoSuchElementException:
        qual = "자격요건 정보를 찾을 수 없습니다."
    try:
        pref = driver.find_element(By.XPATH,"//*[text()='우대사항']/following-sibling::div").text.strip()
    except NoSuchElementException:
        pref = "우대사항 정보를 찾을 수 없습니다."
    try:
        proc = driver.find_element(By.XPATH,"//*[text()='채용절차']/following-sibling::div").text.strip()
    except NoSuchElementException:
        proc = "채용절차 정보를 찾을 수 없습니다."
    try:
        wel_fare =driver.find_element(By.XPATH,"//*[text()='복리후생']/following-sibling::div").text.strip()
    except NoSuchElementException:
        wel_fare = "복리후생 정보를 찾을 수 없습니다."
    try:
        etc = driver.find_element(By.XPATH,"//*[text()='기타']/following-sibling::div").text.strip()
    except NoSuchElementException:
        etc = "기타 정보를 찾을 수 없습니다."
    # 결과 출력
    print('회사 이름:', company_name)
    print('마감일:', deadline)
    print('직무:', job_title)
    print('경력:', experience)
    print('고용형태:', employment_type)
    print('급여:', salary)
    print('스킬:', skills)
    print('회사소개 :',intro_element)
    print('주요업무: ',job_duties)
    print('자격요건: ',qual)
    print('우대사항: ',pref)
    print('채용절차: ',proc)
    print('복리후생: ',wel_fare)
    print('기타: ',etc)
    data.append([company_name,deadline,job_title,experience,employment_type,salary,skills,intro_element,job_duties,qual,pref,proc,wel_fare,etc])
    df = pd.DataFrame(data,
                      columns=['회사 이름', '마감일', '직무', '경력', '고용형태', '급여', '스킬', '회사소개', '주요업무', '자격요건', '우대사항', '채용절차',
                               '복리후생', '기타'])
    df.to_csv('jobplanet.csv', mode='a', header=True, encoding='utf-8-sig')





def repeat(num):
    global count
    for i in num:
        print(count)
        count = count+1
        driver.get(i)
        time.sleep(2)
        summary()



#Functions to move data to database
try:
    init()

    last_page_button = driver.find_element(By.XPATH, "(//div[@class='jply_pagination_ty1']//button)[last()-1]").text
    last_page_button = int(last_page_button)
    for i in range(1, last_page_button+1):
        temp = driver.current_url
        number = []
        while True:
            li_elements = driver.find_elements(By.CSS_SELECTOR, 'li.desc_card_list_unit')
            for li_element in li_elements:
                a_tag = li_element.find_element(By.CSS_SELECTOR, 'a')
                href_value = a_tag.get_attribute("href")
                if href_value not in number:
                    number.append(href_value)
            repeat(number)
            driver.get(temp)
            time.sleep(3)
            button = driver.find_element(By.XPATH, f"//button[text()='{i}']")
            #button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,f"//button[text()='{i}']")))
            actions = ActionChains(driver).move_to_element(button)
            actions.perform()
            time.sleep(3)
            button.click()
            time.sleep(3)
    time.sleep(3)


finally:
    # 작업이 끝난 후에는 웹 드라이버를 종료
    driver.quit()