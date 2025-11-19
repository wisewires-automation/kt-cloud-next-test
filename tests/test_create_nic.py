from playwright.sync_api import Page
from pathlib import Path
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.capture import ScreenshotSession

from pages.nic_page import NICPage

file_name = Path(__file__).stem
log = get_logger(file_name)

def create_nic_scenario(page: Page, log, sc: ScreenshotSession | None = None) -> str:
    """
    Network Interface 생성 테스트
    """
    nic_page = NICPage(page)

    log.info("NIC 생성 팝업 오픈")
    nic_page.open_nic_create()

    log.info("NIC 생성 시작")
    nic_name = nic_page.create_nic(select_network=True)
    
    log.info("NIC 생성 완료 | NIC 이름=%s", nic_name)

    return nic_name

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:

        try:
            login_as_admin(page, log)
            nic_name = create_nic_scenario(page, log, sc)
            sc.snap(page, label=nic_name)
        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] Network Interface 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()