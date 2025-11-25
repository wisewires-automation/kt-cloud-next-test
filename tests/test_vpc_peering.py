import time
from pathlib import Path
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.vpc_peering_page import VPCPeeringPage


file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# VPC Peering 생성 시나리오
# -------------------------
def create_vpc_peering_scenario(page: Page, log, sc: ScreenshotSession) -> str:
    
    vpc_p_page = VPCPeeringPage(page)

    vpc_p_page.open_project()
    vpc_p_page.go_console_menu(S.VPC_P_MENU)
    
    vpc_01 = "QA-VPC-GGYE"
    vpc_02 = "QA-VPC-002"

    log.info("[TC-00] VPC Peering 생성 시작")
    vpc_p_page.open_create_modal(C.VPC_PEERING_CREATE)
    vpc_p_name = vpc_p_page.create_vpc_peering(vpc_01, vpc_02)
    log.info("[TC-00] VPC Peering 생성 완료 | VPC Peering 이름=%s", vpc_p_name)

    time.sleep(5)

    if sc is not None:
        sc.snap(page, label="create_vpc_p")
    
    return vpc_p_name

# -------------------------
# VPC Peering 수정 시나리오
# -------------------------
def update_vpc_peering_scenario(page: Page, log, vpc_p_name: str, new_name: str, sc: ScreenshotSession):
    vpc_p_page = VPCPeeringPage(page)

    vpc_p_page.open_project()
    vpc_p_page.go_console_menu(S.VPC_P_MENU)
    
    log.info("[TC-00] VPC Peering 수정 시작 | VPC Peering 이름=%s", vpc_p_name)
    vpc_p_page.go_link_by_name(name=vpc_p_name)
    vpc_p_name = vpc_p_page.run_rename_flow(new_name=new_name)
    log.info("[TC-00] VPC Peering 수정 완료 | 변경된 VPC Peering 이름=%s", vpc_p_name)

    if sc is not None:
        sc.snap(page, label="update_vpc_p")


# -------------------------
# VPC Peering 삭제 시나리오
# -------------------------
def delete_vpc_peering_scenario(page: Page, log, vpc_p_name: str, sc: ScreenshotSession):
    vpc_p_page = VPCPeeringPage(page)

    vpc_p_page.open_project()
    vpc_p_page.go_console_menu(S.VPC_P_MENU)
    
    log.info("[TC-00] VPC Peering 삭제 시작 | VPC Peering 이름=%s", vpc_p_name)
    vpc_p_page.go_link_by_name(name=vpc_p_name)
    vpc_p_page.open_delete_modal()
    vpc_p_page.run_delete_flow()
    log.info("[TC-00] VPC Peering 삭제 완료")

    time.sleep(3)

    if sc is not None:
        sc.snap(page, label=vpc_p_name)

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 로그인
            login_as_admin(page, log)

            vpc_p_name = "qa-vp-002"

            # VPC Peering 생성
            vpc_p_name = create_vpc_peering_scenario(page, log, sc)

            # VPC Peering  수정
            # update_vpc_peering_scenario(page, log, vpc_p_name, new_name=f"{vpc_p_name}-edited", sc=sc)

            # VPC Peering 삭제
            # delete_vpc_peering_scenario(page, log, vpc_p_name, sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("VPC 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()