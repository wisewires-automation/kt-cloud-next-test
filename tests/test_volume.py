from pathlib import Path
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.capture import ScreenshotSession
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.volume_page import VolumePage

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# Volumn 생성 시나리오
# -------------------------
def create_volume_scenario(page: Page, log, sc: ScreenshotSession) -> str:
    volume_page = VolumePage(page)

    volume_page.open_project()
    volume_page.go_console_menu(S.VOLUME_MENU)

    log.info("[TC-00] Volumn 생성 시작")
    volume_page.open_create_modal(C.VOLUME_CREATE)
    volume_name = volume_page.create_volume()
    log.info("[TC-00] Volumn 생성 완료 | Volumn 이름=%s", volume_name)

    if sc is not None:
        sc.snap(page, label=volume_name)

    return volume_name

# -------------------------
# Volumn 수정 시나리오
# -------------------------
def update_volume_scenario(page: Page, log, volume_name: str, new_name: str, sc: ScreenshotSession):
    volume_page = VolumePage(page)

    # volume_page.open_project()
    # volume_page.go_console_menu(S.VOLUME_MENU)
    
    log.info("[TC-00] Volumn 수정 시작 | Volumn 이름=%s", volume_name)
    volume_page.go_link_by_name(name=volume_name)
    volume_page.run_rename_flow(new_name=new_name)
    log.info("[TC-00] Volumn 수정 완료 | 변경된 Volumn 이름=%s", new_name)

    if sc is not None:
        sc.snap(page, label=volume_name)

# -------------------------
# Volumn 삭제 시나리오
# -------------------------
def delete_volume_scenario(page: Page, log, volume_name: str, sc: ScreenshotSession):
    volume_page = VolumePage(page)
    
    # volume_page.open_project()
    # volume_page.go_console_menu(S.VOLUME_MENU)
    
    log.info("[TC-00] Volumn 삭제 시작 | Volumn 이름=%s", volume_name)
    # subnet_page.go_link_by_name(name=volume_name)
    volume_page.run_delete_flow()
    log.info("[TC-00] Volumn 삭제 완료")

    if sc is not None:
        sc.snap(page, label=volume_name)

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 로그인
            login_as_admin(page, log)

            # Volumn 생성
            volume_name = create_volume_scenario(page, log, sc)

            # Volumn 수정
            update_volume_scenario(page, log, volume_name, new_name=f"{volume_name}-01", sc=sc)

            # Volumn 삭제
            delete_volume_scenario(page, log, volume_name, sc)

        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] Volume 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()