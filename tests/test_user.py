import os
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from utils.users import user_repo
from pages.locators.actions import CreateButtonLocators as C
from pages.auth_page import AuthPage
from pages.user_page import UserPage

load_dotenv()

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# 사용자 생성 시나리오
# -------------------------
def create_user_scenario(page: Page, log, user, sc: ScreenshotSession) -> str:
    auth_page = AuthPage(page)
    user_page = UserPage(page)

    # user_id   = user.id
    # name      = user.name
    # email     = user.email
    # phone     = user.phone
    # password  = user.password

    url      = os.getenv("LOGIN_URL")
    group_id = os.getenv("GROUP_ID")

    user_id   = "testid06"
    name      = "임시계정"
    email     = "testuser@wisewires.com"
    phone     = "01012345678"
    password  = "!1Wjdtmddus"

    log.info("[ADMIN] 관리자 페이지 이동")
    user_page.go_manage_admin()

    log.info("[TC-00] 사용자 생성 시작")
    log.info("        - id=%s, name=%s, email=%s, phone=%s", user_id, name, email, phone)
    user_page.open_create_modal(C.USER_CREATE)
    user_page.create_user(id=user_id, name=name, email=email, phone=phone, password=password)
    log.info("[TC-00] 사용자 생성 완료 | id=%s", user_id)

    sc.snap(page, label="create_user")

    log.info("[IAM] 로그인 페이지로 이동 후 로그인 시작 | LOGIN ID=%s", user_id)
    auth_page.login_iam(url=url, group_id=group_id, user_id=user_id,password=password)
    log.info("[IAM] 로그인 완료")

    sc.snap(page, label="new_user_login")

    return user_id

# -------------------------
# 사용자 수정 시나리오
# -------------------------
def update_user_info_scenario(page: Page, log, sc: ScreenshotSession) -> str:
    user_page = UserPage(page)

    user_id   = "testid01"
    name      = "이름수정"
    email     = "edited@google.com"
    phone     = "01011223344"

    log.info("[ADMIN] 관리자 페이지 이동")
    user_page.go_manage_admin()

    log.info("[TC-00] 사용자 수정 시작 | id=%s", user_id)
    user_page.click_user_row(id=user_id)
    user_page.update_user_info(name=name, email=email, phone=phone)
    log.info("[TC-00] 사용자 수정 완료")

    if sc is not None:
        sc.snap(page, label=user_id)

# -------------------------
# 사용자 비밀번호 변경 시나리오
# -------------------------
def update_user_password_scenario(page: Page, log, sc: ScreenshotSession) -> str:
    user_page = UserPage(page)

    user_id   = "testid01"
    password  = "wW231202##"

    user_page.go_manage_admin()

    log.info("[TC-00] 사용자 비밀번호 변경 시작 | id=%s", user_id)
    user_page.click_user_row(id=user_id)
    user_page.update_user_password(password)
    log.info("[TC-00] 사용자 비밀번호 변경 완료")

    if sc is not None:
        sc.snap(page, label=user_id)

# -------------------------
# 사용자 삭제 시나리오
# -------------------------
def delete_user_scenario(page: Page, log, user, sc: ScreenshotSession):
    user_page = UserPage(page)

    log.info("[ADMIN] 관리자 페이지 이동")
    user_page.go_manage_admin()

    id = "testid05"

    log.info("[TC-00] 사용자 삭제 시작")
    user_page.click_user_row(id=id)
    user_page.click_delete_user()
    user_page.run_delete_flow()
    log.info("[TC-00] 사용자 삭제 완료 | 사용자 ID=%s", id)

    if sc is not None:
        sc.snap(page, label="delete_user")


def main():
    user = user_repo.get("TEMP")
    with create_page(headless=False) as page, \
        ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 관리자 로그인
            login_as_admin(page, log)

            # 사용자 생성
            create_user_scenario(page, log, user, sc)

            # 사용자 수정
            # update_user_info_scenario(page, log, sc)

            # 사용자 비밀변호 변경
            # update_user_password_scenario(page, log, sc)

            # 사용자 삭제
            # delete_user_scenario(page, log, user, sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("사용자 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()