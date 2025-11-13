import pytest, os, time
from dotenv import load_dotenv

from pages.auth_page import AuthPage
from pages.project_page import ProjectPage
from pages.server_page import ServerPage
load_dotenv()

def test_create_vpc(page, log):
    # 1) 로그인
    url   = os.getenv("LOGIN_URL")
    kt_id = os.getenv("KT_USER_ID")
    kt_pw = os.getenv("KT_USER_PW")

    auth = AuthPage(page)

    log.info("[KT] 로그인 시작")
    auth.login_kt(url=url, user_id=kt_id, password=kt_pw)
    log.info("[KT] 로그인 완료")

    time.sleep(2)

    # 2) 프로젝트 진입
    project_page = ProjectPage(page)
    project_name = "TEST_CREATE_SERVER"
    log.info("프로젝트 페이지 진입 | 프로젝트명=%s", project_name)
    project_page.open_project(project_name)

    # 3) 서버 생성
    server_page = ServerPage(page)
    log.info("서버 페이지 진입")
    server_page.create_server(server_name="server-name-01", vpc_name="TEST_VPC_Z9K1")
