""" Key Pair POM """

from playwright.sync_api import Page, expect
from utils.namer import make_name_only_alpha

class KPPage:

    # ===== selector / text 상수 =====
    KP_NAV_BUTTON_NAME = "Key Pair"
    KP_CREATE_BUTTON_NAME = "Key Pair 생성"

    KP_NAME_INPUT = 'input[name="name"]' # Key Pair 이름

    CONFIRM_BUTTON_NAME = "생성"
    CLOSE_BUTTON_NAME = "닫기"

    CREATE_SUCCESS_TEXT = "Key Pair 생성 성공"
    CREATE_FAIL_TEXT = "생성 실패"

    def __init__(self, page: Page):
        self.page = page

        self.kp_nav_button = page.get_by_role("button", name=self.KP_NAV_BUTTON_NAME, exact=True)
        self.kp_create_button = (page.locator("button").filter(has_text=self.KP_CREATE_BUTTON_NAME).first)

        self.name_input = page.locator(self.KP_NAME_INPUT)

        self.confirm_button = page.get_by_role("button", name=self.CONFIRM_BUTTON_NAME, exact=True)
        self.close_button = page.get_by_role("button", name=self.CLOSE_BUTTON_NAME, exact=True)

    # ===== 공통 동작 =====
    def open_kp_create(self, timeout: int = 10000):
        expect(self.kp_nav_button).to_be_visible(timeout=timeout)
        self.kp_nav_button.click()

        expect(self.kp_create_button).to_be_visible(timeout=timeout)
        self.kp_create_button.click()

    def fill_form(self, name: str):
        self.name_input.fill(name)

    def submit_and_close(self, timeout: int = 10000):
        self.confirm_button.first.click()

        success_toast = self.page.get_by_text(self.CREATE_SUCCESS_TEXT)
        fail_toast = self.page.get_by_text(self.CREATE_FAIL_TEXT)
        
        try:
            expect(success_toast).to_be_visible(timeout=timeout)
        except Exception:
            try:
                expect(fail_toast).to_be_visible(timeout=timeout)
                raise AssertionError("Key Pair 생성 실패")
            except Exception:
                raise

        self.close_button.click()

    def create_kp(self, name_prefix: str = "KEY-") -> str:
        kp_name = make_name_only_alpha(prefix=name_prefix)

        self.fill_form(name=kp_name)
        self.submit_and_close()
        return kp_name