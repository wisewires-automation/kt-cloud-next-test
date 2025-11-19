from playwright.sync_api import Page
from pathlib import Path
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.capture import ScreenshotSession

from pages.kp_page import KPPage

file_name = Path(__file__).stem
log = get_logger(file_name)

def create_kp_scenario(page: Page, log, sc: ScreenshotSession | None = None) -> str:
    """
    Key Pair 생성 테스트
    """
    kp_page = KPPage(page)

    log.info("Key Pair 생성 팝업 오픈")
    kp_page.open_kp_create()

    log.info("Key Pair 생성 시작")
    kp_name = kp_page.create_kp()

    log.info("Key Pair 생성 완료 | Key Pair 이름=%s", kp_name)

    return kp_name

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:

        try:
            login_as_admin(page, log)
            kp_name = create_kp_scenario(page, log, sc)
            sc.snap(page, label=kp_name)
        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] Key Pair 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()