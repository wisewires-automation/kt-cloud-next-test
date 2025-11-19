from utils.playwright_helpers import create_page, login_as_admin, open_project 
from utils.logger import get_logger
from utils.capture import ScreenshotSession
from scenarios.server_scenarios import create_server_scenario

log = get_logger("run_create_server")

def main():
    project_name = "QA_TEST_PROJECT"

    with create_page(headless=False) as page,\
        ScreenshotSession(__file__, zip_name="run_create_server") as sc:

        try:
            login_as_admin(page, log)
            open_project(page, project_name, log)
            create_server_scenario(page, log, sc=sc)
        except Exception:
            log.exception("[ERROR] 서버 생성 중 예외 발생")
            sc.snap(page, "error")
            raise

if __name__ == "__main__":
    main()
