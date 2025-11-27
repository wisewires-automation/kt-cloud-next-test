import time
from pathlib import Path
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from utils.users import user_repo
from pages.user_page import UserPage

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# 사용자 생성 시나리오
# -------------------------
def create_user_scenario(page: Page, log, user_id, sc: ScreenshotSession) -> str:
    user_page = UserPage(page)

    # user_id   = "test08"
    name      = "테스트08"
    email     = "test@wisewires.com"
    phone     = "01012345678"
    password  = "!1Wjdtmddus"

    log.info("관리자 페이지로 이동")
    user_page.go_manage_admin()
    log.info("[TC-00] 사용자 생성 시작")
    log.info("        - id=%s, name=%s, email=%s, phone=%s", user_id, name, email, phone)
    user_page.create_user(id=user_id, name=name, email=email, phone=phone, password=password)
    user_page.click_button()
    log.info("[TC-00] 사용자 생성 완료 | id=%s", user_id)

    sc.snap(page, label="create_user", delay_sec=2.0)

    return user_id

# -------------------------
# 사용자 수정 시나리오
# -------------------------
def update_user_info_scenario(page: Page, log, user_id, sc: ScreenshotSession) -> str:
    user_page = UserPage(page)

    # user_id   = "test08"
    name      = "테스트10수정"
    email     = "testedit@wisewires.com"
    phone     = "01011112222"

    # log.info("관리자 페이지로 이동")
    # user_page.go_manage_admin()

    log.info("[TC-00] 사용자 수정 시작 | id=%s", user_id)
    user_page.update_user_info(user_id, name, email, phone)
    log.info("[TC-00] 사용자 수정 완료")

    sc.snap(page, label="update_user", delay_sec=1.0)

# -------------------------
# 사용자 비밀번호 변경 시나리오
# -------------------------
def update_user_password_scenario(page: Page, log, user_id, sc: ScreenshotSession) -> str:
    user_page = UserPage(page)

    # user_id   = "test08"
    password  = "!1Wjdtmdduss"

    # log.info("관리자 페이지로 이동")
    # user_page.go_manage_admin()

    log.info("[TC-00] 사용자 비밀번호 변경 시작 | id=%s", user_id)
    user_page.update_user_password(user_id, password)
    user_page.click_button()
    log.info("[TC-00] 사용자 비밀번호 변경 완료")

    sc.snap(page, label="update_user_pw", delay_sec=1.0)

# -------------------------
# 사용자 삭제 시나리오
# -------------------------
def delete_user_scenario(page: Page, log, user_id, sc: ScreenshotSession):
    user_page = UserPage(page)

    # user_id = "test08"

    # log.info("[관리자 페이지로 이동")
    # user_page.go_manage_admin()

    log.info("[TC-00] 사용자 삭제 시작")
    user_page.delete_user(user_id)
    log.info("[TC-00] 사용자 삭제 완료 | 사용자 ID=%s", id)

    sc.snap(page, label="delete_user", delay_sec=1.0)

def main():
    user = user_repo.get("TEMP")
    with create_page(headless=False) as page, \
        ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:

            user_id = "test04"

            # 관리자 로그인
            login_as_admin(page, log)

            # 사용자 생성
            create_user_scenario(page, log, user_id, sc)

            # 사용자 수정
            # update_user_info_scenario(page, log, user_id, sc)

            # 사용자 비밀변호 변경
            # update_user_password_scenario(page, log, user_id, sc)

            # 사용자 삭제
            delete_user_scenario(page, log, user, user_id, sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("사용자 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()