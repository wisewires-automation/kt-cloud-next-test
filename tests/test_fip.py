from pathlib import Path
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_iam
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from pages.common import ButtonLocators as B
from pages.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.fip_page import FIPPage

from config.project_repo import project_repo

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# Floating IP 생성 테스트
# -------------------------
def create_fip_scenario(page: Page, log, sc: ScreenshotSession, project_name: str):
    fip_page = FIPPage(page)

    log.info("Project 진입 | Project Name=%s", project_name)
    fip_page.open_project(project_name)
    
    log.info("Floating IP 페이지로 이동")
    fip_page.go_console_menu(S.FIP_MENU)

    log.info("[TC-00] Floating IP 생성 시작")
    fip_page.create_fip()
    log.info("[TC-00] Floating IP 생성 완료")

    sc.snap(page, label="create_fip", delay_sec=1.0)

# -------------------------
# Floating IP 삭제 시나리오
# -------------------------
def delete_fip_scenario(page: Page, log, fip_name: str, sc: ScreenshotSession):
    fip_page = FIPPage(page)

    log.info("Floating IP 페이지로 이동")
    fip_page.open_project()
    fip_page.go_console_menu(S.FIP_MENU)

    log.info("[TC-00] Floating IP 삭제 시작")
    fip_page.delete_fip(fip_name)
    log.info("[TC-00] Floating IP 삭제 완료")

    sc.snap(page, label=f"delete_fip", delay_sec=2.0)

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 로그인
            login_as_iam(page, log)

            project_config = project_repo.get("QA_PROJECT_BASE")
            project_name = project_config.name

            fip_name = "727054b1-d513-4b1b-a738-419453589ec8"

            # Floating IP 생성
            create_fip_scenario(page, log, sc, project_name)

            # Floating IP 삭제
            # delete_fip_scenario(page, log, fip_name, sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("Floating IP 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()