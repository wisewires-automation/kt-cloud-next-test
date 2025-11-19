from playwright.sync_api import Page
from pathlib import Path
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.capture import ScreenshotSession

from pages.rt_page import RTPage

file_name = Path(__file__).stem
log = get_logger(file_name)

def create_rt_scenario(page: Page, log, sc: ScreenshotSession | None = None) -> str:
    """
    Route Table 생성 테스트
    - 대상 프로젝트 내에 VPC가 생성되어 있어야 함
    """
    rt_page = RTPage(page)

    log.info("Route Table 생성 팝업 오픈")
    rt_page.open_rt_create()

    log.info("Route Table 생성 시작")
    rt_name = rt_page.create_rt()

    log.info("Route Table 생성 완료 | Route Table 이름=%s", rt_name)

    return rt_name

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:

        try:
            login_as_admin(page, log)
            rt_name = create_rt_scenario(page, log, sc)
            sc.snap(page, label=rt_name)
        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] Route Table 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()