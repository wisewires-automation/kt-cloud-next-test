import time
from pathlib import Path
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from utils.users import user_repo
from pages.locators.actions import CreateButtonLocators as C
from pages.user_page import UserPage

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

    log.info("[TC-00] 사용자 생성 시작")
    log.info("        - id=%s, name=%s, email=%s, phone=%s", user_id, name, email, phone)
    user_page.open_create_modal(C.USER_CREATE)
    user_page.create_user(id=user_id, name=name, email=email, phone=phone, password=password)
    log.info("[TC-00] 사용자 생성 완료 | id=%s", user_id)

    # 사용자 생성된 화면 캡쳐를 위해 추가
    time.sleep(2)

    if sc is not None:
        sc.snap(page, label=user_id)

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

    # 사용자 수정된 화면 캡쳐를 위해 추가
    time.sleep(1)

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

    # 사용자 수정된 화면 캡쳐를 위해 추가
    time.sleep(1)

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

            # 사용자 수정
            # update_user_info_scenario(page, log, sc)

            # 사용자 비밀변호 변경
            update_user_password_scenario(page, log, sc)

            # 사용자 삭제
            delete_user_scenario(page, log, user, sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("사용자 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()