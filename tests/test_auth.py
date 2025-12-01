import pytest, os
from pathlib import Path
from dotenv import load_dotenv
from utils.playwright_helpers import create_page
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from pages.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.auth_page import AuthPage

load_dotenv()

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# KT Cloud 계정 로그인 시나리오
# -------------------------
def test_admin_login(page, log, sc: ScreenshotSession):
    url   = os.getenv("LOGIN_URL")
    kt_id = os.getenv("KT_USER_ID")
    kt_pw = os.getenv("KT_USER_PW")

    if not (url and kt_id and kt_pw):
        pytest.skip("LOGIN_URL, KT_USER_ID, KT_USER_PW 환경변수 설정 필요")

    auth = AuthPage(page)

    log.info("[ADMIN] 로그인 시작 | LOGIN ID=%s", kt_id)
    auth.login_admin(url=url, user_id=kt_id, password=kt_pw)
    log.info("[ADMIN] 로그인 완료")

    sc.snap(page, label="kt_login")
    

# -------------------------
# IAM 계정 로그인 시나리오
# -------------------------
def test_iam_login(page, log, sc: ScreenshotSession):
    url      = os.getenv("LOGIN_URL")
    group_id = os.getenv("GROUP_ID")
    iam_id   = os.getenv("IAM_USER_ID")
    iam_pw   = os.getenv("IAM_USER_PW")

    if not (url and group_id and iam_id and iam_pw):
        pytest.skip("LOGIN_URL, GROUP_ID, IAM_USER_ID, IAM_USER_PW 환경변수 설정 필요")

    auth = AuthPage(page)

    log.info("[IAM] 로그인 시작 | LOGIN ID=%s", iam_id)
    auth.login_iam(url=url, group_id=group_id, user_id=iam_id,password=iam_pw)
    log.info("[IAM] 로그인 완료")

    sc.snap(page, label="iam_login")

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # admin login
            test_admin_login(page, log, sc)

            # iam login
            # test_iam_login(page, log, sc)
            
        except Exception:
            sc.snap(page, "error")
            log.exception("로그인 시나리오 실행 중 예외 발생")
            raise
if __name__ == "__main__":
    main()
