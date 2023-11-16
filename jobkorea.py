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

url = "https://www.jobkorea.co.kr/recruit/joblist?menucode=local&localorder=1"
driver = webdriver.Chrome()
driver.implicitly_wait(3)
driver.get(url)
driver.find_element(By.CSS_SELECTOR,'.btn_tit').click()
time.sleep(3)
def crawling(crawling_url):
    # 새 창 열기
    driver.execute_script("window.open('');")
    # 새로 열린 창으로 스위치
    driver.switch_to.window(driver.window_handles[-1])
    info = {}
    try:
        driver.get(crawling_url)
        wait_new_tab = WebDriverWait(driver, 10)

        # coName 엘리먼트가 로드될 때까지 기다림
        co_name_element = wait_new_tab.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span.coName'))
        )
        co_name = co_name_element.text
        # dt 태그 (항목 이름)와 dd 태그 (항목 값)를 각각 추출
        dt_elements = driver.find_elements(By.CSS_SELECTOR,'.tbList dt')
        dd_elements = driver.find_elements(By.CSS_SELECTOR,'.tbList dd')

        for dt, dd in zip(dt_elements, dd_elements):
            info[dt.text] = dd.text
        print(co_name)
        print(info)
    except Exception as e:
        print(f"Error occurred while loading the page: {e}")
    finally:
        driver.close()
        first_tab = driver.window_handles[0]
        driver.switch_to.window(window_name=first_tab)
        time.sleep(3)
try:
    element = driver.find_element(By.ID, "duty_step1_10031")
    driver.execute_script("arguments[0].click();", element)
    for i in range(1000229, 1000248):
        element = driver.find_element(By.ID, f"duty_step2_{i}")
        driver.execute_script("arguments[0].click();", element)
    driver.find_element(By.ID, 'dev-btn-search').click()
    time.sleep(3)

    # 각 div에서 a 태그의 href 속성을 추출합니다.
    count = 1
    total_jobs_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[@class='tplTabBx jobListTab']//li[@class='on']//span[@data-text='전체']"))
    )
    total_jobs_text = total_jobs_element.text
    total_jobs_number = int(''.join(filter(str.isdigit, total_jobs_text)))
    total_jobs_number = int(total_jobs_number / 40 + 1)

    for i in range(1, total_jobs_number + 1):
        titBx_divs = driver.find_elements(By.CSS_SELECTOR, 'div.titBx')
        for div in titBx_divs[:40]:
            a_tag = div.find_element(By.TAG_NAME,'a')
            href = a_tag.get_attribute('href')
            if href is not None:
                crawling(href)
        if i % 10 == 0:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@class='tplPagination newVer']/p/a[@class='tplBtn btnPgnNext']"))
            )
            next_button.click()
        else:
            page_link_xpath = f"//ul/li/a[@data-page='{i+1}']"
            page_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, page_link_xpath))
            )
            page_link.click()
finally:
    # 웹 드라이버 종료
    driver.quit()
