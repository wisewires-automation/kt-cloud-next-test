from pathlib import Path
from playwright.sync_api import Page
from dotenv import load_dotenv
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.snap_page import SnapPage

load_dotenv()

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# Snapshot 수정 시나리오
# -------------------------
def update_snap_scenario(page: Page, log, snap_name: str, new_name: str, sc: ScreenshotSession):
    snap_page = SnapPage(page)

    snap_page.open_project()
    snap_page.go_console_menu(S.SNAP_MENU)
    
    log.info("[TC-00] Snapshot 수정 시작 | Snapshot 이름=%s", snap_name)
    snap_page.go_link_by_name(name=snap_name)
    snap_page.run_rename_flow(new_name=new_name)
    log.info("[TC-00] Snapshot 수정 완료 | 변경된 Snapshot 이름=%s", new_name)

    if sc is not None:
        sc.snap(page, label=snap_name)

# -------------------------
# Snapshot 삭제 시나리오
# -------------------------
def delete_snap_scenario(page: Page, log, snap_name: str, sc: ScreenshotSession):
    snap_page = SnapPage(page)
    
    snap_page.open_project()
    snap_page.go_console_menu(S.SNAP_MENU)
    
    log.info("[TC-00] Snapshot 삭제 시작 | Snapshot 이름=%s", snap_name)
    snap_page.go_link_by_name(name=snap_name)
    snap_page.open_delete_modal()
    snap_page.run_delete_flow()
    log.info("[TC-00] Snapshot 삭제 완료")

    if sc is not None:
        sc.snap(page, label=snap_name)

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 로그인
            login_as_admin(page, log)

            snap_name = "QA-VSNAP-CGCF"

            # VPC 수정
            # update_snap_scenario(page, log, snap_name, new_name=f"{snap_name}-EDITED", sc=sc)

            # VPC 삭제
            delete_snap_scenario(page, log, snap_name, sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("Snapshot 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()