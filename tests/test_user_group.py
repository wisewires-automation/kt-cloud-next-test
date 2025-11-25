import time
from pathlib import Path
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.user_group_page import UserGroupPage

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# 사용자 그룹 생성 시나리오
# -------------------------
def create_user_group_scenario(page: Page, log, name:str, desc: str, sc: ScreenshotSession):
    group_page = UserGroupPage(page)

    log.info("[ADMIN] 관리자 페이지 이동")
    group_page.go_manage_admin()
    group_page.go_user_group_menu()

    log.info("[TC-00] 사용자 그룹 생성 시작 | 이름=%s, 설명=%s", name, desc)
    group_page.open_create_modal(C.USER_GROUP_CREATE)
    group_page.create_user_group(name, desc)
    log.info("[TC-00] 사용자 그룹 생성 완료")

    # 사용자 생성된 화면 캡쳐를 위해 추가
    time.sleep(2)

    if sc is not None:
        sc.snap(page, label="user_group")

# -------------------------
# 사용자 그룹 삭제 시나리오
# -------------------------
def delete_user_group_scenario(page: Page, log, name: str, sc: ScreenshotSession):
    group_page = UserGroupPage(page)

    log.info("[ADMIN] 관리자 페이지 이동")
    # group_page.go_manage_admin()
    # group_page.go_user_group_menu()

    log.info("[TC-00] 사용자 그룹 삭제 시작")
    group_page.click_user_row(name)
    group_page.click_delete_user_group()
    group_page.run_delete_flow()
    log.info("[TC-00] 사용자 그룹 삭제 완료 | 사용자 그룹 이름=%s", id)

    time.sleep(1)

    if sc is not None:
        sc.snap(page, label="delete_user")

def main():
    with create_page(headless=False) as page, \
        ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 관리자 로그인
            login_as_admin(page, log)

            name="user-group-05"
            desc="사용자 그룹 생성 테스트"

            # 사용자 생성
            create_user_group_scenario(page, log, name, desc, sc)

            # 사용자 삭제
            delete_user_group_scenario(page, log, name, sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("사용자 그룹 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()