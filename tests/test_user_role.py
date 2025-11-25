import time
from pathlib import Path
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.user_page import UserPage
from pages.user_role_page import UserRolePage

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# IAM 사용자 조직 역할 할당 시나리오
# -------------------------
def assign_org_roles_scenario(page: Page, log, sc: ScreenshotSession):
    user_page = UserPage(page)
    role_page = UserRolePage(page)

    user_id = "testid01"

    log.info("[ADMIN] 관리자 페이지 이동")
    user_page.go_manage_admin()

    log.info("[TC-00] IAM 사용자 클릭 | id=%s", user_id)
    user_page.click_user_row(id=user_id)
    role_page.click_role_edit()

    log.info("[TC-00] 조직 역할 선택")
    roles = ["USER_MANAGER", "CLIENT_ADMIN"]
    role_page.assign_org_roles(roles=roles)

    time.sleep(2)

    if sc is not None:
        sc.snap(page, label="assign_org_role")

# -------------------------
# IAM 사용자 프로젝트 역할 할당 시나리오
# -------------------------
def assign_project_roles_scenario(page: Page, log, sc: ScreenshotSession):
    user_page = UserPage(page)
    role_page = UserRolePage(page)

    user_id = "testid01"

    log.info("[ADMIN] 관리자 페이지 이동")
    user_page.go_manage_admin()

    log.info("[TC-00] IAM 사용자 클릭 | id=%s", user_id)
    user_page.click_user_row(id=user_id)
    role_page.click_role_edit()

    log.info("[TC-00] 프로젝트 역할 선택")
    roles = ["BLOCK_STORAGE_VIEWER", "VPC_MANAGER"]
    role_page.assign_project_roles(project_name="QA-PROJECT-001", roles=roles)

    time.sleep(2)

    if sc is not None:
        sc.snap(page, label="assign_project_role")

# -------------------------
# IAM 사용자 역할 해제 시나리오
# -------------------------
def unassign_roles_scenario(page: Page, log, sc: ScreenshotSession):
    user_page = UserPage(page)
    role_page = UserRolePage(page)

    user_id = "testid01"

    log.info("[ADMIN] 관리자 페이지 이동")
    user_page.go_manage_admin()

    log.info("[TC-00] IAM 사용자 클릭 | id=%s", user_id)
    user_page.click_user_row(id=user_id)
    role_page.click_role_edit()

    roles = ["USER_MANAGER", "VPC_MANAGER"]

    log.info("[TC-00] 사용자 역할 해제 시작")
    role_page.unassign_role(roles=roles)

    time.sleep(2)

    if sc is not None:
        sc.snap(page, label="unassign_role")


def main():
    with create_page(headless=False) as page, \
        ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 관리자 로그인
            login_as_admin(page, log)

            # 조직 역할 할당
            # assign_org_roles_scenario(page, log, sc)

            # 프로젝트 역할 할당
            # assign_project_roles_scenario(page, log, sc)

            # 역할 해제
            unassign_roles_scenario(page, log, sc)

        except Exception:
            sc.snap(page, "error")
            log.exception("IAM User 역할관리 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()