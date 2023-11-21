import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyodbc
from selenium.common.exceptions import NoSuchElementException

url = "https://www.wanted.co.kr/wdlist?country=kr&job_sort=job.latest_order&years=-1&locations=all"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome()
driver.implicitly_wait(3)
def get_next_sequence_value(cursor, sequence_name):
    cursor.execute(f"SELECT {sequence_name}.NEXTVAL FROM DUAL")
    result = cursor.fetchone()
    return result[0]

def insert_skill_if_not_exists(cursor, skill_name):
    # 스킬이 이미 존재하는지 확인
    check_query = "SELECT skill_id FROM skills WHERE skill_name = ?"
    cursor.execute(check_query, (skill_name,))
    result = cursor.fetchone()

    if result:
        return result[0]  # 이미 존재하는 스킬의 ID 반환
    else:
        # 새 스킬 ID 생성을 위한 시퀀스 사용
        skill_id = get_next_sequence_value(cursor, "skill_seq")

        # 스킬 삽입
        insert_query = "INSERT INTO skills (skill_id, skill_name) VALUES (?, ?)"
        cursor.execute(insert_query, (skill_id, skill_name))
        return skill_id

def insert_job_skills(cursor, job_id, skills_str):
    skills = skills_str.split(', ')  # 쉼표로 스킬 분리
    for skill in skills:
        skill_id = insert_skill_if_not_exists(cursor, skill)
        # 직업-스킬 관계 삽입
        insert_query = "INSERT INTO job_skills (job_id, skill_id) VALUES (?, ?)"
        cursor.execute(insert_query, (job_id, skill_id))

def insert_job_data(cursor, company_name, job_title, title, skills_str):
    try:
        # 새로운 job ID 생성을 위한 시퀀스 사용
        jobid = get_next_sequence_value(cursor, "job_seq")

        # 직업 삽입
        insert_query = "INSERT INTO job (jobid, company_name, job_title, title) VALUES (?, ?, ?, ?)"
        cursor.execute(insert_query, (jobid, company_name, job_title, title))

        if skills_str is None:
            skills_str = "None"

        insert_job_skills(cursor, jobid, skills_str)
        return True
    except pyodbc.Error as e:
        print(f"Error during database operation: {e}")
        print(company_name)
        print(job_title)
        print(title)
        return False
def database(info):
    conn_str = 'DRIVER={Tibero 6 ODBC Driver};SERVER=15.164.171.29;PORT=8629;DATABASE=tibero;UID=taba;PWD=tibero;'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    count = 0
    try:
        for item in info:
            company_name, job_title, title, skills = item
            if insert_job_data(cursor, company_name, job_title, title, skills):
                print("Data inserted successfully.")
                count += 1
            else:
                print("Duplicate data. Insertion skipped.")
        print(f"삽입 데이터 = {count}")
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
def crawling(crawling_urls,job_title):
    data = []
    for crawling_url in crawling_urls:
        driver.get(crawling_url)
        driver.implicitly_wait(10)
        # 예시: '앱 개발자' 직무 제목 추출
        try:
            title = driver.find_element(By.CSS_SELECTOR, "section.JobHeader_className__HttDA h2").text.strip()
        except NoSuchElementException:
            title = "직무를 찾을 수 없습니다."

        # 예시: 회사 이름 추출
        try:
            company_name = driver.find_element(By.CSS_SELECTOR,
                                           "section.JobHeader_className__HttDA a[data-attribute-id='company__click']").text.strip()
        except NoSuchElementException:
            company_name = "회사를 찾을 수 없습니다."

        # 예시: '주요업무' 섹션의 내용 추출
        try:

            job_duties = driver.find_element(By.CSS_SELECTOR, "section.JobDescription_JobDescription__VWfcb p").text.strip()
        except NoSuchElementException:
            job_duties = "주요업무를 찾을 수 없습니다."

        # 예시: '자격요건' 섹션의 내용 추출
        try:
            qualifications = driver.find_element(By.CSS_SELECTOR,
                                             "section.JobDescription_JobDescription__VWfcb h6:nth-of-type(2) + p").text.strip()
        except NoSuchElementException:
            qualifications = "자격요건을 찾을 수 없습니다."

        # 예시: '우대사항' 섹션의 내용 추출
        try:
            preferred_qualifications = driver.find_element(By.CSS_SELECTOR,
                                                   "section.JobDescription_JobDescription__VWfcb h6:nth-of-type(3) + p").text.strip()
        except NoSuchElementException:
            preferred_qualifications = "우대사항을 찾을 수 없습니다."

        # 혜택 및 복지 섹션의 내용 추출
        try:
            benefits = driver.find_element(By.CSS_SELECTOR,
                                       "section.JobDescription_JobDescription__VWfcb h6:nth-of-type(4) + p").text.strip()
        except NoSuchElementException:
            benefits = "혜택 및 복지를 찾을 수 없습니다."

        # 기술스택 섹션의 내용 추출
        # 기술스택이 여러 개의 div 태그로 나누어져 있을 수 있으므로, 모든 관련 요소를 찾아 텍스트를 합칩니다.
        try:
            tech_stack_elements = driver.find_elements(By.CSS_SELECTOR,
                                                   "div.JobDescription_JobDescription_skill_wrapper__9EdFE div.SkillItem_SkillItem__E2WtM")
            tech_stack = ', '.join([element.text.strip() for element in tech_stack_elements])
        except NoSuchElementException:
            tech_stack = "기술스택을 찾을 수 없습니다."
        # 결과 출력
        # print("회사이름:", company_name)
        # print("직무 제목:", job_title)
        # print("주요업무:", job_duties)
        # print("자격요건:", qualifications)
        # print("우대사항:", preferred_qualifications)
        # print("혜택 및 복지:", benefits)
        # print("기술스택:", tech_stack)
        data.append(
            [company_name, job_title, title, tech_stack])
    return data

def repeat(url,job_title):
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
    info = crawling(data, job_title)
    database(info)
def software_enginner():
    url = "https://www.wanted.co.kr/wdlist/518/10110?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"소프트웨어 개발")
def web_developer():
    url = "https://www.wanted.co.kr/wdlist/518/873?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"웹개발")
def server_developer():
    url = "https://www.wanted.co.kr/wdlist/518/872?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"서버 개발")
def frontend_developer():
    url = "https://www.wanted.co.kr/wdlist/518/669?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"프론트엔드 개발")
def java_developer():
    url = "https://www.wanted.co.kr/wdlist/518/660?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"자바 개발")
def C_Cpp_developer():
    url = "https://www.wanted.co.kr/wdlist/518/900?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"C/C++ 개발")
def python_developer():
    url = "https://www.wanted.co.kr/wdlist/518/899"
    repeat(url,"파이썬 개발")
def machine_learning_developer():
    url = "https://www.wanted.co.kr/wdlist/518/1634?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"머신러닝 개발")
def data_engineer():
    url = "https://www.wanted.co.kr/wdlist/518/655?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"데이터 엔지니어")
def android_developer():
    url = "https://www.wanted.co.kr/wdlist/518/677"
    repeat(url,"안드로이드 개발")
def nodejs_developer():
    url = "https://www.wanted.co.kr/wdlist/518/895"
    repeat(url,"Node.js 개발")
def system_manager():
    url = "https://www.wanted.co.kr/wdlist/518/665?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url, "시스템, 네트워크 관리자")
def devops_manager():
    url = "https://www.wanted.co.kr/wdlist/518/674?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"DevOps 개발")
def ios_developer():
    url = "https://www.wanted.co.kr/wdlist/518/678?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"iOS 개발")
def embedded_developer():
    url = "https://www.wanted.co.kr/wdlist/518/658?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"임베디드 개발")
def development_manager():
    url = "https://www.wanted.co.kr/wdlist/518/877?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"개발 매니저")
def technical_support():
    url = "https://www.wanted.co.kr/wdlist/518/1026?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"기술지원")
def data_scientist():
    url = "https://www.wanted.co.kr/wdlist/518/1024?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"데이터 분석가")
def test_engineer():
    url = "https://www.wanted.co.kr/wdlist/518/676?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"QA(Quality Assurance)")
def security_engineer():
    url = "https://www.wanted.co.kr/wdlist/518/671?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"보안 엔지니어")
def hardware_engineer():
    url = "https://www.wanted.co.kr/wdlist/518/672?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"하드웨어 엔지니어")
def bigdata_engineer():
    url = "https://www.wanted.co.kr/wdlist/518/1025?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"빅데이터 엔지니어")
def product_manager():
    url = "https://www.wanted.co.kr/wdlist/518/876?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"제품 관리자")
def cross_platform_developer():
    url = "https://www.wanted.co.kr/wdlist/518/10111?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"크로스 플랫폼 개발")
def php_developer():
    url = "https://www.wanted.co.kr/wdlist/518/893?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"PHP 개발")
def dba():
    url = "https://www.wanted.co.kr/wdlist/518/10231?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"DBA(Database Admin.)")
def erp_professional():
    url = "https://www.wanted.co.kr/wdlist/518/10230?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"ERP")
def blockchain_flatform_engineer():
    url = "https://www.wanted.co.kr/wdlist/518/1027?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"블록체인 플랫폼 개발자")
def sound_engineer():
    url = "https://www.wanted.co.kr/wdlist/518/896?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"사운드 엔지니어")
def web_publisher():
    url = "https://www.wanted.co.kr/wdlist/518/939?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"웹퍼블리셔")
def dotnet_developer():
    url = "https://www.wanted.co.kr/wdlist/518/661?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,".NET 개발")
def cto():
    url = "https://www.wanted.co.kr/wdlist/518/795?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"CTO (Chief Technology Officer)")
def graphics_engineer():
    url = "https://www.wanted.co.kr/wdlist/518/898?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"그래픽스 엔지니어")
def bi_engineer():
    url = "https://www.wanted.co.kr/wdlist/518/1022?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"BI 엔지니어")
def vr_engineer():
    url = "https://www.wanted.co.kr/wdlist/518/10112?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"VR 엔지니어")
def rubyonrails_developer():
    url = "https://www.wanted.co.kr/wdlist/518/894?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"Ruby on Rails 개발자")
def cio():
    url = "https://www.wanted.co.kr/wdlist/518/793?country=kr&job_sort=job.latest_order&years=-1&locations=all"
    repeat(url,"CIO (Chief Information Officer)")


try:
    # software_enginner()
    # web_developer()
    #server_developer()
    #frontend_developer()
    #java_developer()
    #C_Cpp_developer()
    #python_developer()
    machine_learning_developer()
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
    #test_engineer()
    #security_engineer()
    #hardware_engineer()
    #bigdata_engineer()
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
    #bi_engineer()
    #vr_engineer()
    #rubyonrails_developer()
    #cio()
finally:
    driver.quit()
