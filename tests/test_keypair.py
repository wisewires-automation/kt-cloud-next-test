from pathlib import Path
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.keypair_page import KeypairPage

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# Key Pair 생성 시나리오
# -------------------------
def create_kp_scenario(page: Page, log, sc: ScreenshotSession) -> str:
    kp_page = KeypairPage(page)

    kp_page.open_project()
    kp_page.go_console_menu(S.KP_MENU)

    log.info("[TC-00] Key Pair 생성 시작")
    kp_page.open_create_modal(C.KP_CREATE)
    kp_name = kp_page.create_kp()
    log.info("[TC-00] Key Pair 생성 완료 | Key Pair 이름=%s", kp_name)

    if sc is not None:
        sc.snap(page, label=kp_name)

    return kp_name

# -------------------------
# Key Pair 삭제 시나리오
# -------------------------
def delete_kp_scenario(page: Page, log, kp_name: str, sc: ScreenshotSession):
    kp_page = KeypairPage(page)
    
    # kp_page.open_project()
    # kp_page.go_console_menu(S.KP_MENU)

    log.info("[TC-00] Key Pair 삭제 시작 | Key Pair 이름=%s", kp_name)
    kp_page.delete_kp(kp_name)
    kp_page.run_delete_flow()
    log.info("[TC-00] Key Pair 삭제 완료")

    if sc is not None:
        sc.snap(page, label=kp_name)

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 로그인
            login_as_admin(page, log)

            # Key pair 생성
            kp_name = create_kp_scenario(page, log, sc)

            # Key pair 삭제
            delete_kp_scenario(page, log, kp_name=kp_name, sc=sc)

        except Exception:
            sc.snap(page, "error")
            log.exception("Key Pair 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()