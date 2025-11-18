import os
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from utils.logger import setup_logging, get_logger
from pages.auth_page import AuthPage

load_dotenv()
setup_logging()

def login_as_admin(page, log=None):
    """KT admin 계정으로 로그인 (conftest.kt_logged_in_page와 동일 역할)"""
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


def create_page(headless: bool = False):
    """
    pytest 없이 쓸 때:
    with create_page() as page:
        ...
    형태로 사용 가능한 헬퍼
    """
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
