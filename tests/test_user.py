import time
from pathlib import Path
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.capture import ScreenshotSession
from utils.users import user_repo
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.user_page import UserPage
from pages.role_page import RolePage

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# 사용자 생성 시나리오
# -------------------------
def create_user_scenario(page: Page, log, user, sc: ScreenshotSession) -> str:
    user_page = UserPage(page)

    user_id   = user.id
    name      = user.name
    email     = user.email
    phone     = user.phone
    password  = user.password

    log.info("[ADMIN] 관리자 페이지 이동")
    user_page.go_manage_admin()

    log.info("[TC-00] IAM 사용자 생성 시작")
    log.info("        - id=%s, name=%s, email=%s, phone=%s", user_id, name, email, phone)
    user_page.open_create_modal(C.USER_CREATE)
    user_page.create_user(id=user_id, name=name, email=email, phone=phone, password=password)
    log.info("[TC-00] IAM 사용자 생성 완료 | id=%s", user_id)

    # 사용자 생성된 화면 캡쳐를 위해 추가
    time.sleep(2)

    if sc is not None:
        sc.snap(page, label=user_id)

    return user_id

# -------------------------
# 사용자 권한 부여 시나리오
# -------------------------
def grant_role_scenario(page: Page, log, user, sc: ScreenshotSession):

    user_page = UserPage(page)
    role_page = RolePage(page)

    log.info("[ADMIN] 관리자 페이지 이동")
    user_page.go_manage_admin()

    log.info("[ADMIN] IAM 사용자 클릭 | id=%s", user.id)
    role_page.click_user_row(id=user.id)
    role_page.click_role_edit()

    # log.info("[ADMIN] 라디오 그룹 선택")
    # role_page.click_radio_group(is_org=False)

    log.info("[ADMIN] 역할 선택")
    role_page.click_role_checkbox_by_name("USER_MANAGER")

    time.sleep(5)

    if sc is not None:
        sc.snap(page, label="update_role")

# -------------------------
# 사용자 삭제 시나리오
# -------------------------
def delete_user_scenario(page: Page, log, user, sc: ScreenshotSession):
    user_page = UserPage(page)
    role_page = RolePage(page)

    log.info("[ADMIN] 관리자 페이지 이동")
    user_page.go_manage_admin()

    id = "testid05"

    log.info("[TC-00] 사용자 삭제 시작")
    role_page.click_user_row(id=id)
    user_page.click_delete_user()
    user_page.run_delete_flow()
    log.info("[TC-00] 사용자 삭제 완료 | 사용자 ID=%s", id)

    time.sleep(1)

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
            # create_user_scenario(page, log, user, sc)

            # 사용자 권한 부여
            # grant_role_scenario(page, log, user, sc)

            # 사용자 삭제
            delete_user_scenario(page, log, user, sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] 사용자 예외 발생")
            raise

if __name__ == "__main__":
    main()