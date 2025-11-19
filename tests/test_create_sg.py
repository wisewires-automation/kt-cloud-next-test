from playwright.sync_api import Page
from pathlib import Path
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.capture import ScreenshotSession

from pages.sg_page import SGPage

file_name = Path(__file__).stem
log = get_logger(file_name)

def create_sg_scenario(page: Page, log, sc: ScreenshotSession | None = None) -> str:
    """
    Security Groups 생성 테스트
    """
    sg_page = SGPage(page)

    log.info("Security Groups 생성 팝업 오픈")
    sg_page.open_sg_create()

    log.info("Security Groups 생성 시작")
    sg_name = sg_page.create_sg()

    log.info("Security Groups 생성 완료 | Security Groups 이름=%s", sg_name)

    return sg_name

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:

        try:
            login_as_admin(page, log)
            sg_name = create_sg_scenario(page, log, sc)
            sc.snap(page, label=sg_name)
        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] Network ACL 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()
