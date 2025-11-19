from playwright.sync_api import Page
from pathlib import Path
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.capture import ScreenshotSession

from pages.acl_page import ACLPage

file_name = Path(__file__).stem
log = get_logger(file_name)

def create_acl_scenario(page: Page, log, sc: ScreenshotSession | None = None) -> str:
    """
    Network ACL 생성 테스트
    """
    acl_page = ACLPage(page)

    log.info("Network ACL 생성 팝업 오픈")
    acl_page.open_acl_create()

    log.info("Network ACL 생성 시작")
    acl_name = acl_page.create_acl()

    log.info("Network ACL 생성 완료 | Network ACL 이름=%s", acl_name)

    return acl_name


def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:

        try:
            login_as_admin(page, log)
            acl_name = create_acl_scenario(page, log, sc)
            sc.snap(page, label=acl_name)
        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] Network ACL 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()