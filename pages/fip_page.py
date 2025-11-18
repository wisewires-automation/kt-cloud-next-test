""" Floating IP POM """

from playwright.sync_api import Page, expect

class FIPPage:

    # ===== selector / text 상수 =====
    FIP_NAV_BUTTON_NAME = "Floating IP"
    FIP_CREATE_BUTTON_NAME = "Floating IP 생성"

    CONFIRM_BUTTON_NAME = "생성"
    
    CREATE_SUCCESS_TEXT = "Floating IP가 성공적으로 생성되었습니다."
    CREATE_FAIL_TEXT = "생성 실패"

    def __init__(self, page: Page):
        self.page = page

        self.fip_nav_button = page.get_by_role("button", name=self.FIP_NAV_BUTTON_NAME, exact=True)
        self.fip_create_button = (page.locator("button").filter(has_text=self.FIP_CREATE_BUTTON_NAME).first)

        self.confirm_button = page.get_by_role("button", name=self.CONFIRM_BUTTON_NAME)

    # ===== 공통 동작 =====
    def open_fip_create(self, timeout: int = 10000):
        expect(self.fip_nav_button).to_be_visible(timeout=timeout)
        self.fip_nav_button.click()

        expect(self.fip_create_button).to_be_visible(timeout=timeout)
        self.fip_create_button.click()

    def submit(self, timeout: int = 10000):
        expect(self.confirm_button).to_be_enabled(timeout=timeout)
        self.confirm_button.click()

        success_toast = self.page.get_by_text(self.CREATE_SUCCESS_TEXT)
        fail_toast = self.page.get_by_text(self.CREATE_FAIL_TEXT)
        
        try:
            expect(success_toast).to_be_visible(timeout=timeout)
        except Exception:
            try:
                expect(fail_toast).to_be_visible(timeout=timeout)
                raise AssertionError("Floating IP 생성 실패")
            except Exception:
                raise