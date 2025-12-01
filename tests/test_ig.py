from playwright.sync_api import Page
from pathlib import Path
from utils.playwright_helpers import create_page, login_as_iam
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from pages.actions import SidebarLocators as S
from pages.ig_page import IGPage

from config.project_repo import project_repo

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# Internet Gateway 생성 시나리오
# -------------------------
def create_ig_scenario(page: Page, log, sc: ScreenshotSession, project_name: str) -> str:
    ig_page = IGPage(page)

    log.info("Project 진입 | Project Name=%s", project_name)
    ig_page.open_project(project_name)

    log.info("Internet Gateway 페이지로 이동")
    ig_page.go_console_menu(S.IG_MENU)

    log.info("[TC-00] Internet Gateway 생성 시작")
    created_name = ig_page.create_ig()
    log.info("[TC-00] Internet Gateway 생성 완료 | Internet Gateway 이름=%s", created_name)

    sc.snap(page, label="creat_ig", delay_sec=1.0)

    return created_name

# -------------------------
# Internet Gateway 삭제 시나리오
# -------------------------
def delete_ig_scenario(page: Page, log, ig_name: str, sc: ScreenshotSession):
    ig_page = IGPage(page)

    # log.info("Internet Gateway 페이지로 이동")
    # ig_page.open_project()    
    # ig_page.go_console_menu(S.IG_MENU)
    
    log.info("[TC-00] Internet Gateway 삭제 시작 | Internet Gateway 이름=%s", ig_name)
    ig_page.delete_ig(ig_name)
    log.info("[TC-00] Internet Gateway 삭제 완료")

    sc.snap(page, label="delete_ig", delay_sec=1.0)

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            login_as_iam(page, log)

            project_config = project_repo.get("QA_PROJECT_BASE")

            project_name = project_config.name

            # Internet Gateway 생성
            ig_name = create_ig_scenario(page, log, sc, project_name)
            
            # Internet Gateway 삭제
            delete_ig_scenario(page, log, ig_name, sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("Internet Gateway 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()