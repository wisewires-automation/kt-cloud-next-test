import os
from pathlib import Path
from playwright.sync_api import Page
from dotenv import load_dotenv
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.capture import ScreenshotSession
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.subnet_page import SubnetPage

load_dotenv()

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# Subnet 생성 시나리오
# (필수) VPC가 생성되어 있어야 함
# -------------------------
def create_subnet_scenario(page: Page, log, sc: ScreenshotSession) -> str:
    cidr = os.getenv("CIDR")
    
    subnet_page = SubnetPage(page)

    subnet_page.open_project()
    subnet_page.go_console_menu(S.SUBNET_MENU)
    
    log.info("[TC-00] Subnet 생성 시작")
    subnet_page.open_create_modal(C.SUBNET_CREATE)
    subnet_name = subnet_page.create_subnet(cidr=cidr)
    log.info("[TC-00] Subnet 생성 완료 | Subnet 이름=%s", subnet_name)


    if sc is not None:
        sc.snap(page, label=subnet_name)
    
    return subnet_name

# -------------------------
# Subnet 수정 시나리오
# -------------------------
def update_subnet_scenario(page: Page, log, subnet_name: str, new_name: str, sc: ScreenshotSession):
    subnet_page = SubnetPage(page)

    # subnet_page.open_project()
    # subnet_page.go_console_menu(S.SUBNET_MENU)
    
    log.info("[TC-00] Subnet 수정 시작 | Subnet 이름=%s", subnet_name)
    subnet_page.go_link_by_name(name=subnet_name)
    subnet_name = subnet_page.run_rename_flow(new_name=new_name)
    log.info("[TC-00] Subnet 수정 완료 | 변경된 Subnet 이름=%s", new_name)

    if sc is not None:
        sc.snap(page, label=subnet_name)

# -------------------------
# Subnet 삭제 시나리오
# -------------------------
def delete_subnet_scenario(page: Page, log, subnet_name: str, sc: ScreenshotSession):
    subnet_page = SubnetPage(page)
    
    # subnet_page.open_project()
    # subnet_page.go_console_menu(S.SUBNET_MENU)
    
    log.info("[TC-00] Subnet 삭제 시작 | Subnet 이름=%s", subnet_name)
    # subnet_page.go_link_by_name(name=subnet_name)
    subnet_page.open_delete_modal()
    subnet_page.run_delete_flow()
    log.info("[TC-00] Subnet 삭제 완료")

    if sc is not None:
        sc.snap(page, label=subnet_name)

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 로그인
            login_as_admin(page, log)

            # subnet_name = "QA-SUBNET-A"

            # Subnet 생성
            subnet_name = create_subnet_scenario(page, log, sc)

            # VPC 수정
            update_subnet_scenario(page, log, subnet_name, new_name=f"{subnet_name}-01", sc=sc)

            # VPC 삭제
            delete_subnet_scenario(page, log, subnet_name, sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] Subnet 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()