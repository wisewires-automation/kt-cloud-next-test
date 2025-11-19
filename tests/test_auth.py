import pytest, os
from pathlib import Path
from utils.playwright_helpers import create_page
from utils.capture import ScreenshotSession
from dotenv import load_dotenv

from pages.auth_page import AuthPage

load_dotenv()

file_name = Path(__file__).stem

def test_kt_login(page, log):
    """kt cloud 계정 로그인"""
    url   = os.getenv("LOGIN_URL")
    kt_id = os.getenv("KT_USER_ID")
    kt_pw = os.getenv("KT_USER_PW")

    if not (url and kt_id and kt_pw):
        pytest.skip("LOGIN_URL, KT_USER_ID, KT_USER_PW 환경변수 설정 필요")

    auth = AuthPage(page)

    log.info("[KT] 로그인 시작")
    auth.login_kt(url=url, user_id=kt_id, password=kt_pw)
    log.info("[KT] 로그인 완료")

def test_iam_login(page, log):
    """IAM 계정 로그인"""
    url      = os.getenv("LOGIN_URL")
    group_id = os.getenv("GROUP_ID")
    iam_id   = os.getenv("IAM_USER_ID")
    iam_pw   = os.getenv("IAM_USER_PW")

    if not (url and group_id and iam_id and iam_pw):
        pytest.skip("LOGIN_URL, GROUP_ID, IAM_USER_ID, IAM_USER_PW 환경변수 설정 필요")

    auth = AuthPage(page)

    log.info("[IAM] 로그인 시작")
    auth.login_iam(url=url, group_id=group_id, user_id=iam_id,password=iam_pw)
    log.info("[IAM] 로그인 완료")


def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        sc.snap(page, file_name)

if __name__ == "__main__":
    main()
