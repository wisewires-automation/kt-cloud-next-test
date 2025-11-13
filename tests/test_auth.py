import pytest, os
from pages.auth_page import AuthPage
from dotenv import load_dotenv

load_dotenv()

# kt cloud 계정 로그인
def test_kt_login(page, log):
    url   = os.getenv("LOGIN_URL")
    kt_id = os.getenv("KT_USER_ID")
    kt_pw = os.getenv("KT_USER_PW")

    if not (url and kt_id and kt_pw):
        pytest.skip("LOGIN_URL, KT_USER_ID, KT_USER_PW 환경변수 설정 필요")

    auth = AuthPage(page)

    log.info("[KT] 로그인 시작")
    auth.login_kt(url=url, user_id=kt_id, password=kt_pw)
    log.info("[KT] 로그인 완료")

# IAM 계정 로그인
def test_iam_login(page, log):
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