from playwright.sync_api import Page
from pathlib import Path
from utils.playwright_helpers import create_page, login_as_iam
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from pages.actions import SidebarLocators as S
from pages.sg_page import SGPage

from config.stack_repo import stack_repo
from config.project_repo import project_repo
from config.sg_repo import sg_repo

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# Security Group 생성 시나리오
# -------------------------
def create_sg_scenario(page: Page, log, sc: ScreenshotSession, project_name: str, sg_name: str, desc: str) -> str:
    sg_page = SGPage(page)

    log.info("Project 진입 | Project Name=%s", project_name)
    sg_page.open_project(project_name)

    log.info("Security Group 페이지로 이동")
    sg_page.go_console_menu(S.SG_MENU)
    
    log.info("[TC-00] Security Group 생성 시작")
    created_name = sg_page.create_sg(sg_name, desc)
    log.info("[TC-00] Security Group 생성 완료 | Security Group 이름=%s", sg_name)

    sc.snap(page, label="create_sg", delay_sec=1.0)
    
    return created_name

# -------------------------
# Security Group 수정 시나리오
# -------------------------
def update_sg_scenario(page: Page, log, sc: ScreenshotSession, sg_name: str, new_name: str, desc: str):
    sg_page = SGPage(page)

    # log.info("Network ACL 페이지로 이동")
    # sg_page.open_project()
    # sg_page.go_console_menu(S.SG_MENU)
    
    log.info("[TC-00] Security Group 수정 시작 | Security Group 이름=%s", sg_name)
    sg_page.update_sg(sg_name, new_name, desc)
    log.info("[TC-00] Security Group 수정 완료 | 변경된 Security Group 이름=%s", new_name)

    sc.snap(page, label="update_sg", delay_sec=1.0)

# -------------------------
# Security Group 삭제 시나리오
# -------------------------
def delete_sg_scenario(page: Page, log, sc: ScreenshotSession, sg_name: str):
    sg_page = SGPage(page)

    # log.info("Security Group 페이지로 이동")
    # sg_page.open_project()
    # sg_page.go_console_menu(S.SG_MENU)

    log.info("[TC-00] Security Group 삭제 시작 | Security Group 이름=%s", sg_name)
    sg_page.delete_sg(sg_name)
    log.info("[TC-00] Security Group 삭제 완료")

    sc.snap(page, label="delete_sg", delay_sec=1.0)

# -------------------------
# Security Group - Inbound 생성 시나리오
# -------------------------
def create_inbound_scenario(page: Page, log, sc: ScreenshotSession, sg_name: str):
    sg_page = SGPage(page)

    sg_page.open_project(project_name="QA-PROJECT-001")
    sg_page.go_console_menu(S.SG_MENU)
    
    sg_name = "QA-AUTO-TEST"
    ip = "10.0.0.0/8"
    port = 20

    log.info("[TC-00] Security Group Inbound 생성 시작 | Security Group 이름=%s", sg_name)
    sg_page.create_sg_inbound(sg_name, ip, port)
    log.info("[TC-00] Security Group Inbound 생성 완료")

    sc.snap(page, label="create_sg_inbound", delay_sec=1.0)


def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 로그인
            login_as_iam(page, log)
            
            # YAML에서 정보 가져오기
            # stack = stack_repo.get("TEST_STACK_FOR_SG")
            # project_config = project_repo.get(stack.project_key)
            # sg_config = sg_repo.get(stack.)
   
            project_config = project_repo.get("QA_PROJECT_BASE")
            sg_config = sg_repo.get("QA_SG_AUTO")

            project_name = project_config.name
            sg_name = sg_config.name
            sg_desc = sg_config.description

            # Security Group 생성
            sg_name = create_sg_scenario(page, log, sc, project_name, sg_name, desc=sg_desc)

            # Security Group 수정
            new_name = f"{sg_name}-EDITED"
            sg_name = update_sg_scenario(page, log, sc, sg_name, new_name, desc=sg_desc)

            # Security Group 삭제
            delete_sg_scenario(page, log, sc, sg_name)

            # Inbound 규칙 생성
            # create_inbound_scenario(page, log, sc, sg_name)

        except Exception:
            sc.snap(page, "error")
            log.exception("Security Group 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()
