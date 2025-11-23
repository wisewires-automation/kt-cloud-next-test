from pathlib import Path
from playwright.sync_api import Page
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.capture import ScreenshotSession
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.acl_page import ACLPage

file_name = Path(__file__).stem
log = get_logger(file_name)

# -------------------------
# Network ACL 생성 테스트
# -------------------------
def create_acl_scenario(page: Page, log, sc: ScreenshotSession) -> str:
    acl_page = ACLPage(page)

    acl_page.open_project()
    acl_page.go_console_menu(S.NACL_MENU)
    
    log.info("[TC-00] Network ACL 생성 시작")
    acl_page.open_create_modal(C.NACL_CREATE)
    acl_name = acl_page.create_acl()
    log.info("[TC-00] Network ACL 생성 완료 | Network ACL 이름=%s", acl_name)

    if sc is not None:
        sc.snap(page, label=acl_name)
    
    return acl_name


# -------------------------
# Network ACL 수정 시나리오
# -------------------------
def update_acl_scenario(page: Page, log, acl_name: str, new_name: str, sc: ScreenshotSession):
    acl_page = ACLPage(page)

    acl_page.open_project()
    acl_page.go_console_menu(S.NACL_MENU)
    
    log.info("[TC-00] Network ACL 수정 시작 | Network ACL 이름=%s", acl_name)
    acl_page.go_link_by_name(name=acl_name)
    acl_name = acl_page.run_rename_flow(new_name=new_name)
    log.info("[TC-00] Network ACL 수정 완료 | 변경된 Network ACL 이름=%s", new_name)

    if sc is not None:
        sc.snap(page, label=acl_name)

# -------------------------
# Network ACL 삭제 시나리오
# -------------------------
def delete_acl_scenario(page: Page, log, acl_name: str, sc: ScreenshotSession):
    acl_page = ACLPage(page)

    # acl_page.open_project()
    # acl_page.go_console_menu(S.NACL_MENU)
    
    log.info("[TC-00] Network ACL 삭제 시작 | Network ACL 이름=%s", acl_name)
    # acl_page.go_link_by_name(name=acl_name)
    acl_page.open_delete_modal()
    acl_page.run_delete_flow()
    log.info("[TC-00] Network ACL 삭제 완료")

    if sc is not None:
        sc.snap(page, label=acl_name)

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
            log.exception("[ERROR] Network ACL 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()