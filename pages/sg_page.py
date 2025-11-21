""" Security Group POM """

from playwright.sync_api import Page, expect
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.locators.common import ToastLocators as T, ButtonLocators as B
from utils.namer import make_name

class SGPage:

    SG_NAME_INPUT = 'input[name="name"]'        # Security Group 이름
    SG_DESC_INPUT = 'input[name="description"]' # 설명

    def __init__(self, page: Page):
        self.page = page

        self.sg_nav_button = page.get_by_role("button", name=S.SG_MENU, exact=True)
        self.sg_create_button = (page.locator("button").filter(has_text=C.SG_CREATE).first)

        self.name_input = page.locator(self.SG_NAME_INPUT)
        self.desc_input = page.locator(self.SG_DESC_INPUT)

        self.confirm_button = page.get_by_role("button", name=B.CREATE_BUTTON_NAME)

    def open_sg_create(self, timeout: int = 10000):
        expect(self.sg_nav_button).to_be_visible(timeout=timeout)
        self.sg_nav_button.click()

        expect(self.sg_create_button).to_be_visible(timeout=timeout)
        self.sg_create_button.click()

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
                raise AssertionError("Security Group 생성 실패")
            except Exception:
                raise
    
    def create_sg(self, name_prefix: str = "QA-SG-") -> str:
        ig_name = make_name(prefix=name_prefix)

        self.fill_form(name=ig_name)
        self.submit()
        
        return ig_name