import time
from pathlib import Path
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.capture import ScreenshotSession

from pages.project_page import ProjectPage

file_name = Path(__file__).stem
log = get_logger(file_name)

def create_project_scenario(page: Page, log, prefix: str, sc: ScreenshotSession | None = None) -> str:
    project_page = ProjectPage(page)

    log.info("프로젝트 생성 시작")

    project_name = project_page.create_project(prefix=prefix)
    log.info("프로젝트 생성 완료 | 프로젝트 이름=%s", project_name)

    # 마지막 화면 캡쳐를 위해 추가
    time.sleep(2)

    if sc is not None:
        sc.snap(page, label=project_name)

    return project_name

def main():
    with create_page(headless=False) as page, \
         ScreenshotSession(__file__, zip_name=file_name) as sc:

        try:
            login_as_admin(page, log)
            create_project_scenario(page, log, prefix="QA_PROJECT_", sc=sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] 프로젝트 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()
