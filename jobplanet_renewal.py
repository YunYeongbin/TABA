import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pyodbc
url = "https://www.jobplanet.co.kr/job"
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(3)
driver.get(url)
driver.find_element(By.CSS_SELECTOR, 'button.jply_btn_sm.inner_text.jf_b2').click()


def init():
    # 대기 시간을 10초로 설정하고, filter_depth1 클래스를 가진 요소가 나타날 때까지 대기
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'filter_depth1'))
    )
    # filter_depth1 클래스를 가진 요소 내에서 개발 버튼을 찾아 클릭
    development_button = element.find_element(By.XPATH, '//button[text()="개발"]')
    development_button.click()


def repeat():
    driver.implicitly_wait(3)
    start = time.time()
    last_height = driver.execute_script("return document.body.scrollHeight")
    while time.time() - start < 3600:
        # scrollHeight까지 스크롤
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        # 새로운 내용 로딩될때까지 기다림
        time.sleep(5)
        # 새로운 내용 로딩됐는지 확인
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    wait = WebDriverWait(driver, 10)
    job_links = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, ".recruitment-content .item-card a[href]")
    ))
    print("찾은 링크의 개수:", len(job_links))
    urls = []
    for job_link in job_links:
        href_value = job_link.get_attribute('href')
        urls.append(href_value)
    return urls

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
def back():
    url = "https://www.jobplanet.co.kr/job"
    driver.get(url)
    driver.find_element(By.CSS_SELECTOR, 'button.jply_btn_sm.inner_text.jf_b2').click()
    init()
def apply_filter_and_crawl(job_category):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'filter_depth2'))
    )
    development_button = element.find_element(By.XPATH, f'//label[contains(.//span, "{job_category}")]')
    development_button.click()
    driver.implicitly_wait(3)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'panel_bottom'))
    )
    apply_button = element.find_element(By.XPATH, '//button[text()="적용"]')
    apply_button.click()
    time.sleep(3)
    urls = repeat()
    info = crawling(urls)

    database(info)
    back()

def cto():
    apply_filter_and_crawl("CTO (Chief Technology Officer)")

def dba():
    apply_filter_and_crawl("DBA(Database Admin.)")

def erp():
    apply_filter_and_crawl("ERP")


def ios_developer():
    apply_filter_and_crawl("iOS 개발")

def qa():
    apply_filter_and_crawl("QA(Quality Assurance)")

def vr_engineer():
    apply_filter_and_crawl("VR 엔지니어")
def game_developer():
    apply_filter_and_crawl("게임개발")
def technical_support():
    apply_filter_and_crawl("기술지원")
def network_security_operator():
    apply_filter_and_crawl("네트워크/보안/운영")
def back_end_developer():
    apply_filter_and_crawl("백엔드 개발")
def software_developer():
    apply_filter_and_crawl("소프트웨어 개발")
def software_architect():
    apply_filter_and_crawl("소프트웨어아키텍트")
def android_developer():
    apply_filter_and_crawl("안드로이드 개발")
def web_developer():
    apply_filter_and_crawl("웹개발")
def web_publisher():
    apply_filter_and_crawl("웹퍼블리셔")
def cloud_developer():
    apply_filter_and_crawl("클라우드 개발")
def front_end_developer():
    apply_filter_and_crawl("프론트엔드 개발")
def hardware_developer():
    apply_filter_and_crawl("하드웨어 개발")


def crawling(urls):
    combined_data = []
    sum_data = []
    for url in urls:
        driver.get(url)
        driver.implicitly_wait(10)
        company_name = driver.find_element(By.CSS_SELECTOR, '.company_name a').text.strip()
        title = driver.find_element(By.CSS_SELECTOR,'.ttl').text.strip()
        # try:
        #     deadline = driver.find_element(By.CSS_SELECTOR, '.recruitment-summary__end').text.strip()
        # except NoSuchElementException:
        #     deadline = "마감일을 찾을 수 없습니다."
        # try:
        #     job_title = driver.find_elements(By.CSS_SELECTOR, '.recruitment-summary__dd')[1].text.strip()
        # except NoSuchElementException:
        #     job_title = "직무를 찾을 수 없습니다."
        # try:
        #     experience = driver.find_elements(By.CSS_SELECTOR, '.recruitment-summary__dd')[2].text.strip()
        # except NoSuchElementException:
        #     experience = "경력을 찾을 수 없습니다."
        # try:
        #     location = driver.find_element(By.CSS_SELECTOR, '.recruitment-summary__location').text
        # except NoSuchElementException:
        #     location = "지역을 찾을 수 없습니다."
        # try:
        #     skills = driver.find_elements(By.CSS_SELECTOR, '.recruitment-summary__dd')[5].text.strip()
        # except NoSuchElementException:
        #     skills = "기술을 찾을 수 없습니다."
        #sum_data.append([job_title, skills])
        #sum.append([company_name, deadline, job_title, experience, location, skills])

        try:
            job_title = driver.find_elements(By.CSS_SELECTOR, '.recruitment-summary__dd')[1].text.strip()
            job_titles = job_title.split(",")  # 쉼표로 'job_title' 분리
            try:
                skills = driver.find_elements(By.CSS_SELECTOR, '.recruitment-summary__dd')[5].text.strip()
            except NoSuchElementException:
                skills = "기술을 찾을 수 없습니다."

            for job_title in job_titles:
                sum_data.append([company_name, job_title.strip(), title,  skills])  # 각 'title'과 'skills'를 'sum_data'에 추가
        except NoSuchElementException:
            continue
        recruitment_boxes = driver.find_elements(By.CLASS_NAME, 'recruitment-detail__box')
        # 각 박스의 텍스트를 저장할 리스트 초기화
        recruitment_details = []

        # 각 박스의 텍스트 내용 추출 및 리스트에 저장
        for box in recruitment_boxes[1:]:
            text = box.text
            if "기업 이미지" not in text:  # "기업 이미지"를 포함하지 않는 경우에만 추가
                first_line_end = text.find('\n')
                first_line = text[:first_line_end].strip()
                remaining_text = text[first_line_end:].strip()
                recruitment_details.append(remaining_text)
        #combined_data.append([company_name, deadline, job_title, experience, location, skills] + recruitment_details)
    return sum_data


try:
    init()
    #cto()
    #dba()
    #erp()
    # ios_developer()
    # qa()
    # vr_engineer()
    # game_developer()
    # technical_support()
    # network_security_operator()
    # back_end_developer()
    # software_developer()
    # software_architect()
    # android_developer()
    # web_developer()
    # web_publisher()
    # cloud_developer()
    front_end_developer()
    # hardware_developer()
finally:
    # 작업이 끝난 후에는 웹 드라이버를 종료
    driver.quit()
