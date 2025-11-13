import os, time
from dotenv import load_dotenv

from pages.auth_page import AuthPage
from pages.project_page import ProjectPage
from pages.subnet_page import SubnetPage

load_dotenv()

def test_create_subnet(page, log):
    # 1) 로그인
    url   = os.getenv("LOGIN_URL")
    kt_id = os.getenv("KT_USER_ID")
    kt_pw = os.getenv("KT_USER_PW")

    auth = AuthPage(page)

    log.info("[KT] 로그인 시작")
    auth.login_kt(url=url, user_id=kt_id, password=kt_pw)
    log.info("[KT] 로그인 완료")

    time.sleep(3)

    # 2) 프로젝트 진입
    project_page = ProjectPage(page)
    project_name = "TEST_CREATE_SERVER"
    log.info("프로젝트 페이지 진입 | 프로젝트명=%s", project_name)
    project_page.open_project(project_name)

    # 3) Subnet 생성
    log.info("Subnet 생성 시작")
    cidr = os.getenv("SUBNET_CIDR")
    subnet_page = SubnetPage(page)
    subnet_name = subnet_page.create_vpc(cidr=cidr)
    log.info("Subnet 생성 완료 | Subnet 명=%s", subnet_name)
