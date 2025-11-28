from pathlib import Path
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_iam
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from pages.locators.actions import SidebarLocators as S

from config.stack_repo import stack_repo
from pages.nat_page import NATPage

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# NAT gateway 생성 시나리오
# -------------------------
def create_nat_gateway_scenario(page: Page, log, sc: ScreenshotSession) -> str:

    # YAML에서 정보 가져오기
    stack = stack_repo.get("TEST_STACK_FOR_NATGATEWAY")
    project_name = stack.project_key
    vpc_name = stack.vpc_key
    rut_name = stack.rut_key
    nat_gateway_page = NATPage(page)

    log.info("NAT gateway 페이지로 이동")
    nat_gateway_page.open_project(project_name)
    nat_gateway_page.go_console_menu(S.NAT_MENU)

    log.info("[TC-00] NAT GATEWAY 생성 시작")
    nat_gateway_name = nat_gateway_page.create_nat(vpc_name, rut_name)
    log.info("[TC-00] NAT GATEWAY 생성 완료 | NAT GATEWAY 이름=%s", nat_gateway_name)

    sc.snap(page, label="create_nat_gateway")

    return nat_gateway_name

# -------------------------
# NAT gateway 삭제 시나리오
# -------------------------
def delete_nat_gateway_scenario(page: Page, log, sc: ScreenshotSession, nat_gateway_name) -> str:
    nat_gateway_page = NATPage(page)

    log.info("[TC-00]  NAT GATEWAY  삭제 시작 |  NAT GATEWAY  이름=%s", nat_gateway_name)
    nat_gateway_page.delete_nat(nat_gateway_name)
    log.info("[TC-00]  NAT GATEWAY  삭제 완료")
    sc.snap(page, label="delete_snap", delay_sec=1.0)

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 로그인
            login_as_iam(page, log)

            # nat gateway 생성
            nat_gateway_name = create_nat_gateway_scenario(page, log, sc)

            # nat gateway 삭제
            delete_nat_gateway_scenario(page, log, sc, nat_gateway_name)
        except Exception:
            sc.snap(page, "error")
            log.exception("NAT gateway 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()