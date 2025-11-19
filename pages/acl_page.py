""" Network ACL POM """

from playwright.sync_api import Page, expect
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.locators.common import ToastLocators as T, ButtonLocators as B
from utils.namer import make_name

class ACLPage:

    NAME_INPUT = 'input[name="name"]'        # 네트워크 ACL 이름
    DESC_INPUT = 'input[name="description"]' # 설명

    def __init__(self, page: Page):
        self.page = page

        self.acl_nav_button = page.get_by_role("button", name=S.NACL_MENU, exact=True)
        self.acl_create_button = (page.locator("button").filter(has_text=C.NACL_CREATE).first)
        self.name_input = page.locator(self.NAME_INPUT)
        self.desc_input = page.locator(self.DESC_INPUT)
        self.confirm_button = page.get_by_role("button", name=B.CREATE_BUTTON)

    def open_acl_create(self, timeout: int = 10000):
        expect(self.acl_nav_button).to_be_visible(timeout=timeout)
        self.acl_nav_button.click()

        expect(self.acl_create_button).to_be_visible(timeout=timeout)
        self.acl_create_button.click()

    def fill_form(self, name: str):
        self.name_input.fill(name)

    def submit(self, timeout: int = 10000):
        expect(self.confirm_button).to_be_enabled(timeout=timeout)
        self.confirm_button.click()

        success_toast = self.page.get_by_text(T.CREATE_SUCCESS_TEXT)
        fail_toast = self.page.get_by_text(T.CREATE_FAIL_TEXT)
        
        try:
            expect(success_toast).to_be_visible(timeout=timeout)
        except Exception:
            try:
                expect(fail_toast).to_be_visible(timeout=timeout)
                raise AssertionError("Nework ACL 생성 실패")
            except Exception:
                raise
    
    def create_acl(self, name_prefix: str = "QA-ACL-") -> str:
        ig_name = make_name(prefix=name_prefix)

        self.fill_form(name=ig_name)
        self.submit()
        
        return ig_name