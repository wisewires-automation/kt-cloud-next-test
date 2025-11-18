import os
import time
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from utils.logger import setup_logging, get_logger
from pages.auth_page import AuthPage
from pages.project_page import ProjectPage
from scenarios.server_scenarios import create_server_scenario

load_dotenv()
setup_logging()

log = get_logger("run_create_server")

def login_as_admin(page):
    url   = os.getenv("LOGIN_URL")
    kt_id = os.getenv("KT_USER_ID")
    kt_pw = os.getenv("KT_USER_PW")

    if not (url and kt_id and kt_pw):
        raise RuntimeError("LOGIN_URL, KT_USER_ID, KT_USER_PW 환경변수 설정 필요")

    auth = AuthPage(page)

    log.info("[ADMIN] 로그인 시작")
    auth.login_kt(url=url, user_id=kt_id, password=kt_pw)
    log.info("[ADMIN] 로그인 완료")

    time.sleep(2)

def open_project(page, project_name: str):
    project_page = ProjectPage(page)
    log.info("프로젝트 진입 | 프로젝트 이름=%s", project_name)
    project_page.open_project(project_name)

def main():
    project_name = "QA_TEST_PROJECT"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # admin 로그인
        login_as_admin(page)

        # 대상 프로젝트 진입
        open_project(page, project_name)

        # 서버 생성 시나리오 실행
        server_name = create_server_scenario(page, log)

        context.close()
        browser.close()

if __name__ == "__main__":
    main()
