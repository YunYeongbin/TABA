import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import os
import pyodbc
url = "https://www.wanted.co.kr/wdlist?country=kr&job_sort=job.latest_order&years=-1&locations=all"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(3)
# driver.get(url)
# driver.find_element(By.CSS_SELECTOR,'button.JobGroup_JobGroup__H1m1m').click()
# # "개발" 카테고리의 링크를 찾기 위해 대기합니다.
# development_link = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '개발')]"))
# )
# # 'href' 속성을 가져옵니다.
# development_href = development_link.get_attribute('href')
# driver.get(development_href)
def database(info):
    # 연결 문자열 설정
    conn_str = 'DRIVER={Tibero 6 ODBC Driver};SERVER=15.164.171.29;PORT=8629;DATABASE=tibero;UID=sys;PWD=tibero;'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    # 테이블 생성
    cursor.execute("select * from v$database")
    for row in cursor:
        print(row)
def crawling(crawling_urls):
    data = []
    for crawling_url in crawling_urls:
        driver.get(crawling_url)
        time.sleep(2)
        # 예시: '앱 개발자' 직무 제목 추출
        job_title = driver.find_element(By.CSS_SELECTOR, "section.JobHeader_className__HttDA h2").text.strip()

        # 예시: 회사 이름 추출
        company_name = driver.find_element(By.CSS_SELECTOR,
                                           "section.JobHeader_className__HttDA a[data-attribute-id='company__click']").text.strip()

        # 예시: '주요업무' 섹션의 내용 추출
        job_duties = driver.find_element(By.CSS_SELECTOR, "section.JobDescription_JobDescription__VWfcb p").text.strip()

        # 예시: '자격요건' 섹션의 내용 추출
        qualifications = driver.find_element(By.CSS_SELECTOR,
                                             "section.JobDescription_JobDescription__VWfcb h6:nth-of-type(2) + p").text.strip()

        # 예시: '우대사항' 섹션의 내용 추출
        preferred_qualifications = driver.find_element(By.CSS_SELECTOR,
                                                       "section.JobDescription_JobDescription__VWfcb h6:nth-of-type(3) + p").text.strip()
        # 혜택 및 복지 섹션의 내용 추출
        benefits = driver.find_element(By.CSS_SELECTOR,
                                       "section.JobDescription_JobDescription__VWfcb h6:nth-of-type(4) + p").text.strip()

        # 기술스택 섹션의 내용 추출
        # 기술스택이 여러 개의 div 태그로 나누어져 있을 수 있으므로, 모든 관련 요소를 찾아 텍스트를 합칩니다.
        tech_stack_elements = driver.find_elements(By.CSS_SELECTOR,
                                                   "div.JobDescription_JobDescription_skill_wrapper__9EdFE div.SkillItem_SkillItem__E2WtM")
        tech_stack = ', '.join([element.text.strip() for element in tech_stack_elements])
        # 결과 출력
        # print("회사이름:", company_name)
        # print("직무 제목:", job_title)
        # print("주요업무:", job_duties)
        # print("자격요건:", qualifications)
        # print("우대사항:", preferred_qualifications)
        # print("혜택 및 복지:", benefits)
        # print("기술스택:", tech_stack)
        data.append(
            [company_name, job_title, tech_stack])
    return data
def repeat(url):
    driver.get(url)
    start = time.time()
    last_height = driver.execute_script("return document.body.scrollHeight")
    while time.time() - start < 600:
        # scrollHeight까지 스크롤
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        # 새로운 내용 로딩될때까지 기다림
        time.sleep(4)
        # 새로운 내용 로딩됐는지 확인
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    # 'href' 속성을 갖는 모든 <a> 태그를 찾습니다.
    # 이 예에서는 'data-cy' 속성이 'job-card'인 <div> 태그 내부의 <a> 태그를 찾습니다.
    wait = WebDriverWait(driver, 10)
    job_links = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div[data-cy='job-card'] a[href]")
    ))
    print("찾은 링크의 개수:", len(job_links))
    data = []
    for job_link in job_links:
        href_value = job_link.get_attribute('href')
        data.append(href_value)
    info = crawling(data)
    print(info)
    #database(info)
    time.sleep(3)
def software_enginner():
    url = "https://www.wanted.co.kr/wdlist/518/10110?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def web_developer():
    url = "https://www.wanted.co.kr/wdlist/518/873?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def server_developer():
    url = "https://www.wanted.co.kr/wdlist/518/872?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def frontend_developer():
    url = "https://www.wanted.co.kr/wdlist/518/669?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def java_developer():
    url = "https://www.wanted.co.kr/wdlist/518/660?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def C_Cpp_developer():
    url = "https://www.wanted.co.kr/wdlist/518/900?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def python_developer():
    url = "https://www.wanted.co.kr/wdlist/518/899"
    repeat(url)
def machine_learning_developer():
    url = "https://www.wanted.co.kr/wdlist/518/1634?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def data_engineer():
    url = "https://www.wanted.co.kr/wdlist/518/655?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def android_developer():
    url = "https://www.wanted.co.kr/wdlist/518/677"
    repeat(url)
def nodejs_developer():
    url = "https://www.wanted.co.kr/wdlist/518/895"
    repeat(url)
def system_manager():
    url = "https://www.wanted.co.kr/wdlist/518/665?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def devops_manager():
    url = "https://www.wanted.co.kr/wdlist/518/674?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def ios_developer():
    url = "https://www.wanted.co.kr/wdlist/518/678?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def embedded_developer():
    url = "https://www.wanted.co.kr/wdlist/518/658?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def development_manager():
    url = "https://www.wanted.co.kr/wdlist/518/877?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def technical_support():
    url = "https://www.wanted.co.kr/wdlist/518/1026?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def data_scientist():
    url = "https://www.wanted.co.kr/wdlist/518/1024?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def test_engineer():
    url = "https://www.wanted.co.kr/wdlist/518/676?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def security_engineer():
    url = "https://www.wanted.co.kr/wdlist/518/671?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def hardware_engineer():
    url = "https://www.wanted.co.kr/wdlist/518/672?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def bigdata_engineer():
    url = "https://www.wanted.co.kr/wdlist/518/1025?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def product_manager():
    url = "https://www.wanted.co.kr/wdlist/518/876?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def cross_platform_developer():
    url = "https://www.wanted.co.kr/wdlist/518/10111?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def php_developer():
    url = "https://www.wanted.co.kr/wdlist/518/893?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def dba():
    url = "https://www.wanted.co.kr/wdlist/518/10231?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def erp_professional():
    url = "https://www.wanted.co.kr/wdlist/518/10230?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def blockchain_flatform_engineer():
    url = "https://www.wanted.co.kr/wdlist/518/1027?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def sound_engineer():
    url = "https://www.wanted.co.kr/wdlist/518/896?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def web_publisher():
    url = "https://www.wanted.co.kr/wdlist/518/939?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def dotnet_developer():
    url = "https://www.wanted.co.kr/wdlist/518/661?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def cto():
    url = "https://www.wanted.co.kr/wdlist/518/795?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def graphics_engineer():
    url = "https://www.wanted.co.kr/wdlist/518/898?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def bi_engineer():
    url = "https://www.wanted.co.kr/wdlist/518/1022?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def vr_engineer():
    url = "https://www.wanted.co.kr/wdlist/518/10112?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def rubyonrails_developer():
    url = "https://www.wanted.co.kr/wdlist/518/894?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)
def cio():
    url = "https://www.wanted.co.kr/wdlist/518/793?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url)

try:
    # software_enginner()
    # web_developer()
    # server_developer()
    # frontend_developer()
    # java_developer()
    # C_Cpp_developer()
    # python_developer()
    # machine_learning_developer()
    # data_engineer()
    # android_developer()
    # nodejs_developer()
    # system_manager()
    # devops_manager()
    # ios_developer()
    # embedded_developer()
    # development_manager()
    # technical_support()
    # data_scientist()
    # test_engineer()
    # security_engineer()
    # hardware_engineer()
    # bigdata_engineer()
    # product_manager()
    # cross_platform_developer()
    # php_developer()
    # dba()
    # erp_professional()
    # blockchain_flatform_engineer()
    # sound_engineer()
    # web_publisher()
    # dotnet_developer()
    # cto()
    # graphics_engineer()
    # bi_engineer()
    # vr_engineer()
    rubyonrails_developer()
    cio()
finally:
    driver.quit()
