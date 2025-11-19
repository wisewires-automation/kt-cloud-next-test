import os, time
from dotenv import load_dotenv

from playwright.sync_api import sync_playwright
from utils.logger import setup_logging, get_logger

from pages.auth_page import AuthPage
from pages.project_page import ProjectPage

load_dotenv()
setup_logging()

def login_as_admin(page, log=None):
    log = get_logger("login_as_admin")

    """admin 계정으로 로그인"""
    url   = os.getenv("LOGIN_URL")
    kt_id = os.getenv("KT_USER_ID")
    kt_pw = os.getenv("KT_USER_PW")

    if not (url and kt_id and kt_pw):
        raise RuntimeError("LOGIN_URL, KT_USER_ID, KT_USER_PW 환경변수 설정 필요")

    auth = AuthPage(page)

    if log:
        log.info("[ADMIN] 로그인 시작")
    auth.login_kt(url=url, user_id=kt_id, password=kt_pw)
    if log:
        log.info("[ADMIN] 로그인 완료")

    time.sleep(2)
    return page

def login_as_iam(page, log=None, user_id: str = ""):
    """IAM 계정으로 로그인"""
    log = get_logger("login_as_iam")

    auth = AuthPage(page)

    if log:
        log.info("[IAM] 로그인 시작 | 아이디=%s", user_id)
    if log:
        log.info("[IAM] 로그인 완료")

    return page

def open_project(page, log=None, project_name: str = "QA_TEST_PROJECT"):
    """proejct 진입"""
    log = get_logger("open_project")

    project_page = ProjectPage(page)

    log.info("프로젝트 진입 | 프로젝트 이름=%s", project_name)
    project_page.open_project(project_name)

    return page

def create_page(headless: bool = False):
    from contextlib import contextmanager

    @contextmanager
    def _cm():
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context()
            page = context.new_page()
            try:
                yield page
            finally:
                context.close()
                browser.close()

    return _cm()
