from utils.logger import get_logger
from utils.playwright_helpers import create_page, login_as_admin
from utils.capture import ScreenshotSession

from scenarios.project_scenarios import create_project_scenario

log = get_logger("run_create_project")

def main():

    with create_page(headless=False) as page, \
         ScreenshotSession(__file__, zip_name="run_create_project") as sc:

        try:
            login_as_admin(page, log)
            create_project_scenario(page, log, prefix="QA_PROJECT_", sc=sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] 프로젝트 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()
