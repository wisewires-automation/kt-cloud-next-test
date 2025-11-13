import os, time
from dotenv import load_dotenv

from pages.auth_page import AuthPage
from pages.project_page import ProjectPage

load_dotenv()

def test_create_project(page, log):
    # 1) 로그인
    url   = os.getenv("LOGIN_URL")
    kt_id = os.getenv("KT_USER_ID")
    kt_pw = os.getenv("KT_USER_PW")

    auth = AuthPage(page)

    log.info("[KT] 로그인 시작")
    auth.login_kt(url=url, user_id=kt_id, password=kt_pw)
    log.info("[KT] 로그인 완료")

    time.sleep(3)

    # 2) 프로젝트 생성
    log.info("프로젝트 생성 시작")
    project_page = ProjectPage(page)
    project_name = project_page.create_project(prefix="TEST_PROJECT_")
    log.info("프로젝트 생성 완료 | 프로젝트명=%s", project_name)
