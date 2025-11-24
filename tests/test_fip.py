from pathlib import Path
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.capture import ScreenshotSession
from pages.locators.common import ButtonLocators as B
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.fip_page import FIPPage

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# Floating IP 생성 테스트
# -------------------------
def create_fip_scenario(page: Page, log, sc: ScreenshotSession):
    fip_page = FIPPage(page)

    fip_page.open_project()
    fip_page.go_console_menu(S.FIP_MENU)

    log.info("[TC-00] Floating IP 생성 시작")
    fip_page.open_create_modal(C.FIP_CREATE)
    fip_page.submit(text=B.CREATE_TEXT)
    log.info("[TC-00] Floating IP 생성 완료")

    if sc is not None:
        sc.snap(page, label="fip-created")

# -------------------------
# Floating IP 삭제 시나리오
# -------------------------
def delete_fip_scenario(page: Page, log, id: str, sc: ScreenshotSession):
    fip_page = FIPPage(page)

    fip_page.open_project()
    fip_page.go_console_menu(S.FIP_MENU)

    log.info("[TC-00] Floating IP 삭제 시작")
    fip_page.go_link_by_name(name=id)
    fip_page.open_delete_modal()
    fip_page.run_delete_flow()
    log.info("[TC-00] Floating IP 삭제 완료")

    if sc is not None:
        sc.snap(page, label=f"delete_fip")

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 로그인
            login_as_admin(page, log)

            # Floating IP 생성
            # create_fip_scenario(page, log, sc)

            id = "c3ff0cb9-e936-441f-8157-99c2c5ce5497"
            # Floating IP 삭제
            delete_fip_scenario(page, log, id, sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] Floating IP 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()