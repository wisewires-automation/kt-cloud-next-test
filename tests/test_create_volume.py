from playwright.sync_api import Page
from pathlib import Path
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.capture import ScreenshotSession

from pages.volume_page import VolumePage

file_name = Path(__file__).stem
log = get_logger(file_name)

def create_volume_scenario(page: Page, log, sc: ScreenshotSession | None = None) -> str:
    """
    Volume 생성 테스트
    """
    volume_page = VolumePage(page)

    log.info("Volume 생성 시작")
    volume_name = volume_page.create_volume()

    log.info("Volume 생성 완료 | Volume 이름=%s", volume_name)

    return volume_name

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:

        try:
            login_as_admin(page, log)
            volume_name = create_volume_scenario(page, log, sc)
            sc.snap(page, label=volume_name)
        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] Volume 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()