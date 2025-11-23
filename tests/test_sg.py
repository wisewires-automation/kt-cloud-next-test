from playwright.sync_api import Page
from pathlib import Path
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.capture import ScreenshotSession
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.sg_page import SGPage

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# Security Group 생성 시나리오
# -------------------------
def create_sg_scenario(page: Page, log, sc: ScreenshotSession) -> str:
    sg_page = SGPage(page)

    sg_page.open_project()
    sg_page.go_console_menu(S.SG_MENU)
    
    log.info("[TC-00] Security Group 생성 시작")
    sg_page.open_create_modal(C.SG_CREATE)
    sg_name = sg_page.create_sg()
    log.info("[TC-00] Security Group 생성 완료 | Security Group 이름=%s", sg_name)

    if sc is not None:
        sc.snap(page, label=sg_name)
    
    return sg_name

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 로그인
            login_as_admin(page, log)

            # Security Group 생성
            sg_name = create_sg_scenario(page, log, sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] Security Group 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()
