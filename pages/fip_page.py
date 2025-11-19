""" Floating IP POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.locators.common import ToastLocators as T, ButtonLocators as B

class FIPPage:
    
    CREATE_SUCCESS_TEXT = "Floating IP가 성공적으로 생성되었습니다."

    def __init__(self, page: Page):
        self.page = page

        self.fip_nav_button = page.get_by_role("button", name=S.FIP_MENU, exact=True)
        self.fip_create_button = (page.locator("button").filter(has_text=C.FIP_CREATE).first)
        self.confirm_button = page.get_by_role("button", name=B.CREATE_CONFIRM_BUTTON)

    def open_fip_create(self, timeout: int = 10000):
        expect(self.fip_nav_button).to_be_visible(timeout=timeout)
        self.fip_nav_button.click()

        expect(self.fip_create_button).to_be_visible(timeout=timeout)
        self.fip_create_button.click()

    def submit(self, timeout: int = 10000):
        expect(self.confirm_button).to_be_enabled(timeout=timeout)
        self.confirm_button.click()

        success_toast = self.page.get_by_text(self.CREATE_SUCCESS_TEXT)
        fail_toast = self.page.get_by_text(T.CREATE_FAIL_TEXT)
        
        try:
            expect(success_toast).to_be_visible(timeout=timeout)
        except Exception:
            try:
                expect(fail_toast).to_be_visible(timeout=timeout)
                raise AssertionError("Floating IP 생성 실패")
            except Exception:
                raise