import time
from playwright.sync_api import Page
from pathlib import Path
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.capture import ScreenshotSession

from pages.fip_page import FIPPage

file_name = Path(__file__).stem
log = get_logger(file_name)

def create_fip_scenario(page: Page, log):
    """
    Floating IP 생성 테스트
    """
    fip_page = FIPPage(page)

    log.info("Floating IP 생성 팝업 오픈")
    fip_page.open_fip_create()

    log.info("Floating IP 생성")
    fip_page.submit()
    
    time.sleep(3)

    log.info("Floating IP 생성 완료")

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:

        try:
            login_as_admin(page, log)
            create_fip_scenario(page, log)
            sc.snap(page, label="floating_ip")
        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] Floating IP 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()