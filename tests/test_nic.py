from playwright.sync_api import Page
from pathlib import Path
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from pages.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.nic_page import NICPage

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# NIC 생성 시나리오
# -------------------------
def create_nic_scenario(page: Page, log, sc: ScreenshotSession) -> str:
    nic_page = NICPage(page)

    log.info("Network ACL 페이지로 이동")
    nic_page.open_project()
    nic_page.go_console_menu(S.NIC_MENU)

    log.info("[TC-00] VPC 생성 시작")
    nic_name = nic_page.create_nic(select_network=True)
    log.info("[TC-00] NIC 생성 완료 | NIC 이름=%s", nic_name)

    sc.snap(page, label="create_nic")

    return nic_name

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 로그인
            login_as_admin(page, log)

            # NIC 생성
            nic_name = create_nic_scenario(page, log, sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("Network Interface 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()