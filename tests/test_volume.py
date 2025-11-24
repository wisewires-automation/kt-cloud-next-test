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
# Volume 생성 시나리오
# -------------------------
def create_volume_scenario(page: Page, log, sc: ScreenshotSession) -> str:
    volume_page = VolumePage(page)

    volume_page.open_project()
    volume_page.go_console_menu(S.VOLUME_MENU)

    log.info("[TC-00] Volumn 생성 시작")
    volume_page.open_create_modal(C.VOLUME_CREATE)
    volume_name = volume_page.create_volume(desc="test volume 설명입니다", size="128")
    log.info("[TC-00] Volumn 생성 완료 | Volume 이름=%s", volume_name)

    if sc is not None:
        sc.snap(page, label=volume_name)

    return volume_name

# -------------------------
# Volume 삭제 시나리오
# -------------------------
def delete_volume_scenario(page: Page, log, volume_name: str, sc: ScreenshotSession):
    volume_page = VolumePage(page)
    
    # volume_page.open_project()
    # volume_page.go_console_menu(S.VOLUME_MENU)
    
    log.info("[TC-00] Volume 삭제 시작 | Volume 이름=%s", volume_name)
    volume_page.delete_volume(volume_name)
    volume_page.run_delete_flow()
    log.info("[TC-00] Volume 삭제 완료")

    if sc is not None:
        sc.snap(page, label=volume_name)

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 로그인
            login_as_admin(page, log)

            # Volumn 생성
            volume_name = create_volume_scenario(page, log, sc)

            # Volumn 삭제
            delete_volume_scenario(page, log, volume_name, sc)

        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] Volume 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()