""" Key Pair POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.locators.common import ButtonLocators as B
from utils.namer import make_name_only_alpha

class KeypairPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    NAME_INPUT = 'input[name="name"]'    # Key Pair 이름
    CREATE_SUCCESS_TEXT = "Key Pair 생성 성공"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    # ============================================================
    # PROPERTIES (locator 객체를 반환)
    # ============================================================ 
    @property
    def name_input(self):
        """모달 - Key Pair 이름 입력 필드"""
        return self.page.locator(self.NAME_INPUT)
    
    @property
    def confirm_button(self):
        return self.page.get_by_role("button", name=B.CREATE_TEXT, exact=True).first
    
    @property
    def close_button(self):
        return self.page.get_by_role("button", name=B.CLOSE_TEXT, exact=True).first
    
    # ============================================================
    # ACTIONS
    # ============================================================
    def fill_form(self, name: str):
        self.name_input.fill(name)

    def click_confirm_button(self, timeout: int = 10000):
        confirm_btn = self.confirm_button.first
        expect(confirm_btn).to_be_enabled(timeout=timeout)
        confirm_btn.click()
    
    def click_close_button(self, timeout: int = 10000):
        close_btn = self.close_button
        expect(close_btn).to_be_enabled(timeout=timeout)
        close_btn.click()

    def get_row_by_name(self, name: str):
        return self.page.locator(f'div[role="row"][row-id="{name}"]').first

    def open_row_menu(self, kp_name: str, timeout: int = 10000):
        row = self.get_row_by_name(kp_name)
        expect(row).to_be_visible(timeout=timeout)

        menu_btn = row.locator('button[data-slot="dropdown-menu-trigger"]').first
        expect(menu_btn).to_be_enabled(timeout=timeout)
        menu_btn.click()

    def click_delete_in_menu(self, timeout: int = 10000):
        delete_item = self.page.get_by_role("menuitem", name="삭제")
        expect(delete_item).to_be_visible(timeout=timeout)
        delete_item.click()

    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_kp(self) -> str:
        kp_name = make_name_only_alpha(prefix="QA-KEY-")
        
        self.fill_form(name=kp_name)
        self.click_confirm_button()
        self.click_close_button()

        return kp_name

    def delete_kp(self, kp_name: str):
        self.open_row_menu(kp_name=kp_name)
        self.click_delete_in_menu()