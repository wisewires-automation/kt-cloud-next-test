import os, time
from pathlib import Path
from playwright.sync_api import Page
from dotenv import load_dotenv
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.vpc_page import VPCPage

load_dotenv()

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# VPC 생성 시나리오
# -------------------------
def create_vpc_scenario(page: Page, log, sc: ScreenshotSession) -> str:
    cidr = os.getenv("CIDR")
    
    vpc_page = VPCPage(page)

    vpc_page.open_project()
    vpc_page.go_console_menu(S.VPC_MENU)
    
    log.info("[TC-00] VPC 생성 시작")
    vpc_page.open_create_modal(C.VPC_CREATE)
    vpc_name = vpc_page.create_vpc(cidr=cidr)
    log.info("[TC-00] VPC 생성 완료 | VPC 이름=%s", vpc_name)

    if sc is not None:
        sc.snap(page, label=vpc_name)
    
    return vpc_name

# -------------------------
# VPC 수정 시나리오
# -------------------------
def update_vpc_scenario(page: Page, log, vpc_name: str, new_name: str, sc: ScreenshotSession):
    vpc_page = VPCPage(page)

    vpc_page.open_project()
    vpc_page.go_console_menu(S.VPC_MENU)
    
    log.info("[TC-00] VPC 수정 시작 | VPC 이름=%s", vpc_name)
    vpc_page.go_link_by_name(name=vpc_name)
    vpc_name = vpc_page.run_rename_flow(new_name=new_name)
    log.info("[TC-00] VPC 수정 완료 | 변경된 VPC 이름=%s", new_name)

    if sc is not None:
        sc.snap(page, label=vpc_name)


# -------------------------
# VPC 삭제 시나리오
# -------------------------
def delete_vpc_scenario(page: Page, log, vpc_name: str, sc: ScreenshotSession):
    vpc_page = VPCPage(page)

    # vpc_page.open_project()
    # vpc_page.go_console_menu(S.VPC_MENU)
    
    log.info("[TC-00] VPC 삭제 시작 | VPC 이름=%s", vpc_name)
    # vpc_page.go_link_by_name(name=vpc_name)
    vpc_page.open_delete_modal()
    vpc_page.run_delete_flow()
    log.info("[TC-00] VPC 삭제 완료")

    time.sleep(3)

    if sc is not None:
        sc.snap(page, label=vpc_name)

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 로그인
            login_as_admin(page, log)

            vpc_name = "QA-VPC-GGYE"
            # VPC 생성
            # vpc_name = create_vpc_scenario(page, log, sc)

            # VPC 수정
            update_vpc_scenario(page, log, vpc_name, new_name=f"{vpc_name}-003", sc=sc)

            # VPC 삭제
            # delete_vpc_scenario(page, log, vpc_name, sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("VPC 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()