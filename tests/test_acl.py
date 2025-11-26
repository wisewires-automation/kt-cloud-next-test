from pathlib import Path
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.screenshot import ScreenshotSession
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.acl_page import ACLPage

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# Network ACL 생성 테스트
# -------------------------
def create_acl_scenario(page: Page, log, sc: ScreenshotSession) -> str:
    acl_page = ACLPage(page)

    log.info("Network ACL 페이지로 이동")
    acl_page.open_project()
    acl_page.go_console_menu(S.NACL_MENU)
    
    log.info("[TC-00] Network ACL 생성 시작")
    acl_name = acl_page.create_acl()
    log.info("[TC-00] Network ACL 생성 완료 | Network ACL 이름=%s", acl_name)

    sc.snap(page, label="create_acl")
    
    return acl_name


# -------------------------
# Network ACL 수정 시나리오
# -------------------------
def update_acl_scenario(page: Page, log, acl_name: str, new_name: str, sc: ScreenshotSession):
    acl_page = ACLPage(page)

    log.info("Network ACL 페이지로 이동")
    acl_page.open_project()
    acl_page.go_console_menu(S.NACL_MENU)
    
    log.info("[TC-00] Network ACL 수정 시작 | Network ACL 이름=%s", acl_name)
    acl_page.update_acl(acl_name, new_name)
    log.info("[TC-00] Network ACL 수정 완료 | 변경된 Network ACL 이름=%s", new_name)

    sc.snap(page, label="update_acl")

# -------------------------
# Network ACL 삭제 시나리오
# -------------------------
def delete_acl_scenario(page: Page, log, acl_name: str, sc: ScreenshotSession):
    acl_page = ACLPage(page)

    log.info("Network ACL 페이지로 이동")
    # acl_page.open_project()
    # acl_page.go_console_menu(S.NACL_MENU)
    
    log.info("[TC-00] Network ACL 삭제 시작 | Network ACL 이름=%s", acl_name)
    acl_page.delete_acl(acl_name)
    log.info("[TC-00] Network ACL 삭제 완료")

    sc.snap(page, label="delete_acl")

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:
        try:
            # 로그인
            login_as_admin(page, log)

            # Network ACL 생성
            acl_name = create_acl_scenario(page, log, sc)

            # Network ACL 수정
            update_acl_scenario(page, log, acl_name, new_name=f"{acl_name}-003", sc=sc)

            # Network ACL 삭제
            # delete_acl_scenario(page, log, acl_name, sc)

        except Exception:
            sc.snap(page, "error")
            log.exception("Network ACL 시나리오 실행 중 예외 발생")
            raise

if __name__ == "__main__":
    main()