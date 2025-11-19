from playwright.sync_api import Page
from pathlib import Path
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.capture import ScreenshotSession

from pages.ig_page import IGPage

file_name = Path(__file__).stem
log = get_logger(file_name)

def create_ig_scenario(page: Page, log, sc: ScreenshotSession | None = None) -> str:
    """
    Internet Gateway 생성 테스트
    """
    ig_page = IGPage(page)

    log.info("Internet Gateway 생성 팝업 오픈")
    ig_page.open_ig_create()

    log.info("Internet Gateway 생성 시작")
    ig_name = ig_page.create_ig()

    log.info("Internet Gateway 생성 완료 | Internet Gateway 이름=%s", ig_name)

    return ig_name

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            login_as_admin(page, log)
            ig_name = create_ig_scenario(page, log, sc)
            sc.snap(page, label=ig_name)
        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] Internet Gateway 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()