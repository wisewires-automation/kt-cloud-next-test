from pathlib import Path
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_iam
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from pages.locators.actions import SidebarLocators as S
from pages.subnet_page import SubnetPage

from config.project_repo import project_repo
from config.vpc_repo import vpc_repo
from config.subnet_repo import subnet_repo
from config.stack_repo import stack_repo

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# Subnet 생성 시나리오
# (필수) VPC가 생성되어 있어야 함
# -------------------------
def create_subnet_scenario(page: Page, log, sc: ScreenshotSession) -> str:
    
    # YAML에서 정보 가져오기
    stack = stack_repo.get("TEST_STACK_FOR_SUBNET")
    project_config = project_repo.get(stack.project_key)
    vpc_config = vpc_repo.get(stack.vpc_key)
    subnet_config = subnet_repo.get(stack.subnet_key)

    project_name = project_config.name
    vpc_name     = vpc_config.name
    subnet_name  = subnet_config.name
    cidr         = subnet_config.cidr
    
    subnet_page = SubnetPage(page)

    log.info("Project 진입 | Project Name=%s", project_name)
    subnet_page.open_project(project_name)

    log.info("Subnet 페이지로 이동")
    subnet_page.go_console_menu(S.SUBNET_MENU)
    
    log.info("[TC-00] Subnet 생성 시작")
    created_name = subnet_page.create_subnet(vpc_name, subnet_name, cidr)
    log.info("[TC-00] Subnet 생성 완료 | Subnet 이름=%s", created_name)

    sc.snap(page, label="create_subnet", delay_sec=1.0)
    
    return created_name

# -------------------------
# Subnet 수정 시나리오
# -------------------------
def update_subnet_scenario(page: Page, log, subnet_name: str, new_name: str, sc: ScreenshotSession) -> str:
    subnet_page = SubnetPage(page)

    # log.info("Subnet 페이지로 이동")
    # subnet_page.open_project()
    # subnet_page.go_console_menu(S.SUBNET_MENU)
    
    log.info("[TC-00] Subnet 수정 시작 | Subnet 이름=%s", subnet_name)
    subnet_page.update_subnet(subnet_name, new_name)
    log.info("[TC-00] Subnet 수정 완료 | 변경된 Subnet 이름=%s", new_name)

    sc.snap(page, label="update_subnet", delay_sec=1.0)

    return new_name

# -------------------------
# Subnet 삭제 시나리오
# -------------------------
def delete_subnet_scenario(page: Page, log, subnet_name: str, sc: ScreenshotSession):
    subnet_page = SubnetPage(page)
    
    # log.info("Subnet 페이지로 이동")
    # subnet_page.open_project()
    # subnet_page.go_console_menu(S.SUBNET_MENU)
    
    log.info("[TC-00] Subnet 삭제 시작 | Subnet 이름=%s", subnet_name)
    subnet_page.delete_subnet(subnet_name)
    log.info("[TC-00] Subnet 삭제 완료")

    sc.snap(page, label="delete_snap", delay_sec=1.0)

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 로그인
            login_as_iam(page, log)

            # Subnet 생성
            subnet_name = create_subnet_scenario(page, log, sc)

            # VPC 수정
            new_name = f"{subnet_name}-EDITED"
            subnet_name = update_subnet_scenario(page, log, subnet_name, new_name, sc)

            # VPC 삭제
            delete_subnet_scenario(page, log, subnet_name, sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("subnet 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()