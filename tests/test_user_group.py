import time
from pathlib import Path
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from pages.user_group_page import UserGroupPage

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# 사용자 그룹 생성 시나리오
# -------------------------
def create_user_group_scenario(page: Page, log, name:str, desc: str, sc: ScreenshotSession):
    group_page = UserGroupPage(page)

    log.info("사용자 그룹 페이지로 이동")
    group_page.go_manage_admin()
    group_page.go_user_group_menu()

    log.info("[TC-00] 사용자 그룹 생성 시작 | 이름=%s, 설명=%s", name, desc)
    group_page.create_user_group(name, desc)
    log.info("[TC-00] 사용자 그룹 생성 완료")

    sc.snap(page, label="create_user_group", delay_sec=1.0)

# -------------------------
# 사용자 그룹 삭제 시나리오
# -------------------------
def delete_user_group_scenario(page: Page, log, group_name: str, sc: ScreenshotSession):
    group_page = UserGroupPage(page)

    # log.info("사용자 그룹 페이지로 이동")
    # group_page.go_manage_admin()
    # group_page.go_user_group_menu()

    log.info("[TC-00] 사용자 그룹 삭제 시작")
    group_page.delete_user_group(group_name)
    log.info("[TC-00] 사용자 그룹 삭제 완료 | 사용자 그룹 이름=%s", group_name)

    sc.snap(page, label="delete_user_group")

# -------------------------
# 사용자 그룹 멤버 추가 시나리오
# -------------------------
def add_group_member_scenario(page: Page, log, group_name: str, sc: ScreenshotSession):
    group_page = UserGroupPage(page)

    log.info("사용자 그룹 페이지로 이동")
    group_page.go_manage_admin()
    group_page.go_user_group_menu()

    log.info("[TC-00] 사용자 그룹 멤버 추가 시작")
    user_ids = ["187a48da-aa78-48c0-ac90-8b1ab27b7d24", "2816a086-a09b-431e-8b40-405be7f9301e"]
    group_page.add_group_member(group_name, user_ids)
    log.info("[TC-00] 사용자 그룹 멤버 추가 완료")

    sc.snap(page, label="add_group_member", delay_sec=1.0)

# -------------------------
# 사용자 그룹 멤버 삭제 시나리오
# -------------------------
def delete_group_member_scenario(page: Page, log, group_name: str, sc: ScreenshotSession):
    group_page = UserGroupPage(page)

    log.info("사용자 그룹 페이지로 이동")
    group_page.go_manage_admin()
    group_page.go_user_group_menu()

    log.info("[TC-00] 사용자 그룹 멤버 삭제 시작")
    user_ids = ["187a48da-aa78-48c0-ac90-8b1ab27b7d24", "2816a086-a09b-431e-8b40-405be7f9301e"]
    group_page.delete_group_member(group_name, user_ids)
    log.info("[TC-00] 사용자 그룹 멤버 삭제 완료")

    sc.snap(page, label="delete_group_member", delay_sec=1.0)

def main():
    with create_page(headless=False) as page, \
        ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 관리자 로그인
            login_as_admin(page, log)

            name="user-group-01"
            desc="사용자 그룹 생성 테스트"

            # 사용자 그룹 생성
            # create_user_group_scenario(page, log, name, desc, sc)

            # 사용자 그룹 삭제
            # delete_user_group_scenario(page, log, name, sc)

            # 사용자 그룹 멤버 추가
            add_group_member_scenario(page, log, group_name=name, sc=sc)

            # 사용자 그룹 멤버 삭제
            # delete_group_member_scenario(page, log, group_name=name, sc=sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("사용자 그룹 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()