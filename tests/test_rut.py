from playwright.sync_api import Page
from pathlib import Path
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from utils.screenshot import ScreenshotSession

from pages.rut_page import RUTPage

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# Route Table 생성 시나리오
# -------------------------
def create_rut_scenario(page: Page, log, sc: ScreenshotSession) -> str:
    rut_page = RUTPage(page)

    log.info("Route Table 페이지로 이동")
    rut_page.open_project()
    rut_page.go_console_menu(S.RUT_MENU)
    
    log.info("[TC-00] Route Table 생성 시작")
    rut_name = rut_page.create_rut(desc="", vpc_name="")
    log.info("[TC-00] Route Table 생성 완료 | Route Table 이름=%s", rut_name)
    
    sc.snap(page, label=rut_name)

    return rut_name

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 로그인
            login_as_admin(page, log)

            # Route Table 생성
            rut_name = create_rut_scenario(page, log, sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("Route Table 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()