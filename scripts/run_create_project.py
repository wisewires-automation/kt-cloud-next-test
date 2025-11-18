from utils.logger import get_logger
from utils.playwright_helpers import create_page, login_as_admin
from scenarios.project_scenarios import create_project_scenario

def main():
    log = get_logger("run_create_project")

    # with context manager로 page 생성
    with create_page(headless=False) as page:
        # 1) admin 로그인
        login_as_admin(page, log)

        # 2) 프로젝트 생성
        project_name = create_project_scenario(page, log, prefix="QA_PROJECT_")
        log.info("[SCRIPT] 최종 생성된 프로젝트 이름 = %s", project_name)

        input("브라우저를 닫으려면 엔터를 누르세요...")

if __name__ == "__main__":
    main()
