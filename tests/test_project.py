import time
from pathlib import Path
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from pages.locators.actions import SidebarLocators as S
from pages.project_page import ProjectPage
from config.project_repo import project_repo

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# 프로젝트 생성 시나리오
# -------------------------
def create_project_scenario(page: Page, log, sc: ScreenshotSession, name: str, desc: str) -> str:
    project_page = ProjectPage(page)

    log.info("프로젝트 관리하기 페이지로 이동")
    project_page.go_manage_project()

    log.info("[TC-00] 프로젝트 생성 시작")
    created_name = project_page.create_project(name, desc)
    log.info("[TC-00] 프로젝트 생성 완료 | 프로젝트 이름=%s", created_name)

    sc.snap(page, label="create_project", delay_sec=2.0)

    return created_name

# -------------------------
# 프로젝트 수정 시나리오
# -------------------------
def update_project_scenario(page: Page, log, sc: ScreenshotSession, project_name: str, new_name: str, desc: str) -> str:
    project_page = ProjectPage(page)

    # log.info("프로젝트 관리하기 페이지로 이동")
    # project_page.go_manage_admin()
    # project_page.go_admin_menu(S.MANAGE_PROJECT_MENU)                

    log.info("[TC-00] 프로젝트 수정 시작 | 프로젝트 이름=%s", project_name)
    project_page.update_project(project_name, new_name, desc)
    log.info("[TC-00] 프로젝트 수정 완료 | 변경된 프로젝트 이름=%s", new_name)
    
    sc.snap(page, label="update_project", delay_sec=1.0)

    return new_name

# -------------------------
# 프로젝트 삭제 시나리오
# -------------------------
def delete_project_scenario(page: Page, log, sc: ScreenshotSession,  project_name: str):
    project_page = ProjectPage(page)

    # log.info("프로젝트 관리하기 페이지로 이동")
    # project_page.go_manage_project()

    log.info("[TC-00] 프로젝트 삭제 시작 | 프로젝트 이름=%s", project_name)
    project_page.delete_project(project_name=project_name)
    log.info("[TC-00] 프로젝트 삭제 완료")

    sc.snap(page, label="delete_project", delay_sec=1.0)

def main():
    with create_page(headless=False) as page, \
         ScreenshotSession(__file__, zip_name=file_name) as sc:

        try:
            # 로그인
            login_as_admin(page, log)

            # YAML에서 VPC 정보 가져오기
            project_config = project_repo.get("QA_PROJECT_AUTO")
            name = project_config.name
            desc = project_config.description

            # 프로젝트 생성
            project_name = create_project_scenario(page, log, sc, name, desc)

            time.sleep(1)
            # 프로젝트 수정
            new_name = f"{project_name}-EDITED"
            print(f'new_name :{new_name}')
            new_desc = "프로젝트 설명 수정"
            project_name = update_project_scenario(page, log, sc, project_name, new_name, desc=new_desc)

            # 프로젝트 삭제
            delete_project_scenario(page, log, sc, project_name)
            
        except Exception:
            sc.snap(page, "error")
            log.exception("프로젝트 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()
