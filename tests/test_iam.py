import time
from pathlib import Path
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.iam_user_config import get_iam_user
from utils.capture import ScreenshotSession

from pages.user.user_page import UserPage
from pages.role_page import RolePage

file_name = Path(__file__).stem
log = get_logger(file_name)

def create_iam_user_scenario(page: Page, log, iam_user_info: dict, sc: ScreenshotSession | None = None) -> str:
    """
    ADMIN 계정에서 IAM 사용자 생성 시나리오
    """
    user_page = UserPage(page)

    log.info("[ADMIN] 관리자 페이지 이동")
    user_page.go_manage_admin()

    user_id   = iam_user_info["id"]
    name      = iam_user_info["name"]
    email     = iam_user_info["email"]
    phone     = iam_user_info["phone"]
    password  = iam_user_info["password"]

    log.info("[ADMIN] IAM 사용자 생성 시작")
    log.info("        - id=%s, name=%s, email=%s, phone=%s", user_id, name, email, phone)

    user_page.create_user(id=user_id, name=name, email=email, phone=phone, password=password,)

    log.info("[ADMIN] IAM 사용자 생성 완료 | id=%s", user_id)

    return user_id

def test_grant_role(kt_logged_in_page, iam_user_info, log):
    """
    ADMIN 계정에서 IAM 사용자 권한 부여
    """
    page = kt_logged_in_page

    user_page = UserPage(page)
    role_page = RolePage(page)

    id = iam_user_info["id"]

    log.info("[ADMIN] 관리자 페이지 이동")
    user_page.go_manage_admin()

    log.info("[ADMIN] IAM 사용자 클릭 | id=%s", id)
    role_page.click_user_row(id=id)
    role_page.click_role_edit()

    # log.info("[ADMIN] 라디오 그룹 선택")
    # role_page.click_radio_group(is_org=False)

    log.info("[ADMIN] 역할 선택")
    role_page.click_role_checkbox_by_name("USER_MANAGER")

    time.sleep(5)


def main():
    iam_user_info = get_iam_user("TEMP")

    log.info("생성 예정 IAM 계정 | id=%s", iam_user_info["id"],)

    with create_page(headless=False) as page, \
        ScreenshotSession(__file__, zip_name=file_name) as sc:

        try:
            login_as_admin(page, log)
            create_iam_user_scenario(page, log, iam_user_info, sc)
            sc.snap(page, label="create_user")
        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] IAM 계정 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()