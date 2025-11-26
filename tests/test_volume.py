import time
from pathlib import Path
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.volume_page import VolumePage

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# Volume 생성 시나리오
# -------------------------
def create_volume_scenario(page: Page, log, sc: ScreenshotSession) -> str:
    volume_page = VolumePage(page)

    log.info("Volume 페이지로 이동")
    volume_page.open_project()
    volume_page.go_console_menu(S.VOLUME_MENU)

    log.info("[TC-00] Volumn 생성 시작")
    volume_name = volume_page.create_volume(desc="test volume 설명입니다", size="128")
    log.info("[TC-00] Volumn 생성 완료 | Volume 이름=%s", volume_name)

    sc.snap(page, label="create_volume")

    return volume_name

# -------------------------
# Volume 용량 확장 시나리오
# -------------------------
def update_volume_size_scenario(page: Page, log, volume_name: str, size: str, sc: ScreenshotSession):
    volume_page = VolumePage(page)

    log.info("Volume 페이지로 이동")
    volume_page.open_project()
    volume_page.go_console_menu(S.VOLUME_MENU)

    log.info("[TC-00] Volumn 용량 확장 시작")
    volume_page.update_volume_size(volume_name=volume_name, size=size)
    log.info("[TC-00] Volumn 용량 확장 완료 | Volume 이름=%s", volume_name)

    sc.snap(page, label="update_volume_size")

# -------------------------
# Volume Image 생성 시나리오
# -------------------------
def create_volume_image_scenario(page: Page, log, volume_name: str, sc: ScreenshotSession) -> str:
    volume_page = VolumePage(page)

    log.info("Volume 페이지로 이동")
    volume_page.open_project()
    volume_page.go_console_menu(S.VOLUME_MENU)

    log.info("[TC-00] Volumn Image 생성 시작")
    volume_image_name = volume_page.create_volume_image(volume_name=volume_name, desc="test volume image 설명입니다")
    log.info("[TC-00] Volumn Image 생성 완료 | Volume Image 이름=%s", volume_image_name)

    sc.snap(page, label="creaet_volume_img")

    return volume_image_name

# -------------------------
# Volume Snapshot 생성 시나리오
# -------------------------
def create_volume_snapshot_scenario(page: Page, log, volume_name: str, sc: ScreenshotSession) -> str:
    volume_page = VolumePage(page)

    log.info("Volume 페이지로 이동")
    volume_page.open_project()
    volume_page.go_console_menu(S.VOLUME_MENU)

    log.info("[TC-00] Volumn Snapshot 생성 시작")
    volume_snap_name = volume_page.create_volume_snapshot(volume_name=volume_name, desc="test volume snapshot 설명입니다")
    log.info("[TC-00] Volumn Snapshot 생성 완료 | Volume Snapshot 이름=%s", volume_snap_name)

    sc.snap(page, label="create_volume_snap")

    return volume_snap_name

# -------------------------
# Volume 삭제 시나리오
# -------------------------
def delete_volume_scenario(page: Page, log, volume_name: str, sc: ScreenshotSession):
    volume_page = VolumePage(page)
    
    # log.info("Volume 페이지로 이동")
    # volume_page.open_project()
    # volume_page.go_console_menu(S.VOLUME_MENU)
    
    log.info("[TC-00] Volume 삭제 시작 | Volume 이름=%s", volume_name)
    volume_page.delete_volume(volume_name)
    log.info("[TC-00] Volume 삭제 완료")

    sc.snap(page, label="delete_volume")

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 로그인
            login_as_admin(page, log)

            volume_name = "QA-VOL-001"
            # Volumn 생성
            # volume_name = create_volume_scenario(page, log, sc)

            # Volumn 용량 확장
            update_volume_size_scenario(page, log, volume_name=volume_name, size="256", sc=sc)

            # Volumn Image 생성
            # create_volume_image_scenario(page, log, volume_name=volume_name, sc=sc)

            # Volumn Snapshot 생성
            # create_volume_snapshot_scenario(page, log, volume_name=volume_name, sc=sc)

            # Volumn 삭제
            # delete_volume_scenario(page, log, volume_name, sc)

        except Exception:
            sc.snap(page, "error")
            log.exception("Volume 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()