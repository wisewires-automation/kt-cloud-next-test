from pathlib import Path
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.nacl_page import ACLPage

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# Network ACL 생성 테스트
# -------------------------
def create_nacl_scenario(page: Page, log, sc: ScreenshotSession) -> str:
    acl_page = ACLPage(page)

    log.info("Network ACL 페이지로 이동")
    acl_page.open_project()
    acl_page.go_console_menu(S.NACL_MENU)
    
    log.info("[TC-00] Network ACL 생성 시작")
    nacl_name = acl_page.create_nacl()
    log.info("[TC-00] Network ACL 생성 완료 | Network ACL 이름=%s", nacl_name)

    sc.snap(page, label="create_acl", delay_sec=1.0)
    
    return nacl_name

# -------------------------
# Network ACL 수정 시나리오
# -------------------------
def update_nacl_scenario(page: Page, log, nacl_name: str, new_name: str, sc: ScreenshotSession):
    acl_page = ACLPage(page)

    # log.info("Network ACL 페이지로 이동")
    # acl_page.open_project()
    # acl_page.go_console_menu(S.NACL_MENU)
    
    log.info("[TC-00] Network ACL 수정 시작 | Network ACL 이름=%s", nacl_name)
    acl_page.update_nacl(nacl_name, new_name)
    log.info("[TC-00] Network ACL 수정 완료 | 변경된 Network ACL 이름=%s", new_name)

    sc.snap(page, label="update_acl", delay_sec=1.0)

# -------------------------
# Network ACL 삭제 시나리오
# -------------------------
def delete_nacl_scenario(page: Page, log, nacl_name: str, sc: ScreenshotSession):
    acl_page = ACLPage(page)

    # log.info("Network ACL 페이지로 이동")
    # acl_page.open_project()
    # acl_page.go_console_menu(S.NACL_MENU)
    
    log.info("[TC-00] Network ACL 삭제 시작 | Network ACL 이름=%s", nacl_name)
    acl_page.delete_nacl(nacl_name)
    log.info("[TC-00] Network ACL 삭제 완료")

    sc.snap(page, label="delete_acl", delay_sec=1.0)

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 로그인
            login_as_admin(page, log)

            # nacl_name = "QA-ACL"

            # Network ACL 생성
            nacl_name = create_nacl_scenario(page, log, sc)

            new_name = f"{nacl_name}-EDITED"

            # Network ACL 수정
            update_nacl_scenario(page, log, nacl_name, new_name=new_name, sc=sc)

            # Network ACL 삭제
            delete_nacl_scenario(page, log, nacl_name, sc)

        except Exception:
            sc.snap(page, "error")
            log.exception("Network ACL 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()