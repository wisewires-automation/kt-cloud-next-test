from pathlib import Path
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_iam
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from pages.locators.actions import SidebarLocators as S
from pages.vpc_page import VPCPage

from config.project_repo import project_repo
from config.vpc_repo import vpc_repo
from config.stack_repo import stack_repo

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# VPC 생성 시나리오
# -------------------------
def create_vpc_scenario(
        page: Page, 
        log, 
        sc: ScreenshotSession, 
        project_name: str, 
        vpc_name: str, 
        cidr: str) -> str:
    vpc_page = VPCPage(page)

    log.info("Project 진입 | Project Name=%s", project_name)
    vpc_page.open_project(project_name)

    log.info("VPC 페이지로 이동")
    vpc_page.go_console_menu(S.VPC_MENU)
    
    log.info("[TC-00] VPC 생성 시작")
    created_name = vpc_page.create_vpc(vpc_name, cidr)
    log.info("[TC-00] VPC 생성 완료 | VPC 이름=%s", vpc_name)

    sc.snap(page, label="create_vpc", delay_sec=1.0)

    return created_name

# -------------------------
# VPC 수정 시나리오
# -------------------------
def update_vpc_scenario(page: Page, log, sc: ScreenshotSession, vpc_name: str, new_name: str) -> str:
    vpc_page = VPCPage(page)

    # log.info("VPC 페이지로 이동")
    # vpc_page.open_project()
    # vpc_page.go_console_menu(S.VPC_MENU)
    
    log.info("[TC-00] VPC 수정 시작 | VPC 이름=%s", vpc_name)
    vpc_page.update_vpc(vpc_name, new_name)
    log.info("[TC-00] VPC 수정 완료 | 변경된 VPC 이름=%s", new_name)

    sc.snap(page, label="update_vpc", delay_sec=1.0)

    return new_name

# -------------------------
# VPC 삭제 시나리오
# -------------------------
def delete_vpc_scenario(page: Page, log, vpc_name: str, sc: ScreenshotSession):
    vpc_page = VPCPage(page)

    # log.info("VPC 페이지로 이동")
    # vpc_page.open_project()
    # vpc_page.go_console_menu(S.VPC_MENU)
    
    log.info("[TC-00] VPC 삭제 시작 | VPC 이름=%s", vpc_name)
    vpc_page.delete_vpc(vpc_name)
    log.info("[TC-00] VPC 삭제 완료")

    sc.snap(page, label="delete_vpc", delay_sec=2.0)

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:

            # 로그인
            login_as_iam(page, log)

            # YAML에서 정보 가져오기
            stack = stack_repo.get("TEST_STACK_FOR_VPC")
            project_config = project_repo.get(stack.project_key)
            vpc_config = vpc_repo.get(stack.vpc_key)

            project_name = project_config.name
            vpc_name = vpc_config.name
            cidr     = vpc_config.cidr 

            # VPC 생성
            vpc_name = create_vpc_scenario(page, log, sc, project_name, vpc_name, cidr)

            # VPC 수정
            new_name = f"{vpc_name}-EDITED"
            vpc_name = update_vpc_scenario(page, log, sc, vpc_name, new_name)

            # VPC 삭제
            delete_vpc_scenario(page, log, vpc_name, sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("VPC 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()