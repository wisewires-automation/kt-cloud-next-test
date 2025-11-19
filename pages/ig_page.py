""" Internet Gateway POM """

from playwright.sync_api import Page, expect
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.locators.common import ToastLocators as T, ButtonLocators as B
from utils.namer import make_name

class IGPage:

    NAME_INPUT = 'input[name="name"]' # Internet Gateway 이름

    def __init__(self, page: Page):
        self.page = page

        self.ig_nav_button = page.get_by_role("button", name=S.IG_MENU, exact=True)
        self.ig_create_button = (page.locator("button").filter(has_text=C.IG_CREATE).first)
        self.name_input = page.locator(self.NAME_INPUT)
        self.confirm_button = page.get_by_role("button", name=B.CREATE_BUTTON)

    def open_ig_create(self, timeout: int = 10000):
        expect(self.ig_nav_button).to_be_visible(timeout=timeout)
        self.ig_nav_button.click()

        expect(self.ig_create_button).to_be_visible(timeout=timeout)
        self.ig_create_button.click()

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
                raise AssertionError("Internet Gateway 생성 실패")
            except Exception:
                raise
    
    def create_ig(self, name_prefix: str = "QA-IG-") -> str:
        ig_name = make_name(prefix=name_prefix)
        self.fill_form(name=ig_name)
        self.submit()
        return ig_name