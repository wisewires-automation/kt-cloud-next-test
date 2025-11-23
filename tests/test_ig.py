from playwright.sync_api import Page
from pathlib import Path
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.capture import ScreenshotSession
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.ig_page import IGPage

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# Internet Gateway 생성 시나리오
# -------------------------
def create_ig_scenario(page: Page, log, sc: ScreenshotSession) -> str:
    ig_page = IGPage(page)

    ig_page.open_project()
    ig_page.go_console_menu(S.IG_MENU)

    log.info("[TC-00] Internet Gateway 생성 시작")
    ig_page.open_create_modal(C.IG_CREATE)
    ig_name = ig_page.create_ig()
    log.info("[TC-00] Internet Gateway 생성 완료 | Internet Gateway 이름=%s", ig_name)

    if sc is not None:
        sc.snap(page, label=ig_name)

    return ig_name

# -------------------------
# Internet Gateway 수정 시나리오
# -------------------------
def update_ig_scenario(page: Page, log, ig_name: str, new_name: str, sc: ScreenshotSession):
    ig_page = IGPage(page)

    ig_page.open_project()
    ig_page.go_console_menu(S.IG_MENU)
    
    log.info("[TC-00] Internet Gateway 수정 시작 | Internet Gateway 이름=%s", ig_name)
    ig_page.go_link_by_name(name=ig_name)
    ig_name = ig_page.run_rename_flow(new_name=new_name)
    log.info("[TC-00] Internet Gateway 수정 완료 | 변경된 Internet Gateway 이름=%s", new_name)

    if sc is not None:
        sc.snap(page, label=ig_name)

# -------------------------
# Internet Gateway 삭제 시나리오
# -------------------------
def delete_ig_scenario(page: Page, log, ig_name: str, sc: ScreenshotSession):
    ig_page = IGPage(page)

    # ig_page.open_project()
    # ig_page.go_console_menu(S.IG_MENU)
    
    log.info("[TC-00] Internet Gateway 삭제 시작 | Internet Gateway 이름=%s", ig_name)
    # ig_page.go_link_by_name(name=ig_name)
    ig_page.open_delete_modal()
    ig_page.run_delete_flow()
    log.info("[TC-00] Internet Gateway 삭제 완료")

    if sc is not None:
        sc.snap(page, label=ig_name)

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            login_as_admin(page, log)
            # Internet Gateway 생성
            ig_name = create_ig_scenario(page, log, sc)

            # Internet Gateway 수정
            update_ig_scenario(page, log, ig_name, new_name=f"{ig_name}-003", sc=sc)
            
            # Internet Gateway 삭제
            # delete_ig_scenario(page, log, ig_name, sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] Internet Gateway 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()