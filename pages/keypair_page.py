""" Key Pair POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.common import ButtonLocators as B
from pages.actions import CreateButtonLocators as C
from utils.name_generator import generate_name

class KeypairPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    NAME_INPUT = 'input[name="name"]'           # Key Pair 이름 입력 필드 셀렉터
    CREATE_SUCCESS_TEXT = "Key Pair 생성 성공"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    # ============================================================
    # PROPERTIES
    # ============================================================ 
    @property
    def name_input(self):
        """Key Pair 생성 모달 - 이름 입력 필드 locator"""
        return self.page.locator(self.NAME_INPUT)
    
    @property
    def confirm_button(self):
        """Key Pair 생성 모달 - 생성(확인) 버튼 locator"""
        return self.page.get_by_role("button", name=B.CREATE_TEXT, exact=True).first
    
    @property
    def close_button(self):
        """Key Pair 생성 모달 - 닫기 버튼 locator"""
        return self.page.get_by_role("button", name=B.CLOSE_TEXT, exact=True).first
    
    # ============================================================
    # ACTIONS
    # ============================================================
    def click_confirm_button(self, timeout: int = 10000):
        """생성(확인) 버튼 클릭"""
        confirm_btn = self.confirm_button.first
        expect(confirm_btn).to_be_enabled(timeout=timeout)
        confirm_btn.click()
    
    def click_close_button(self, timeout: int = 10000):
        """닫기 버튼 클릭"""
        close_btn = self.close_button
        expect(close_btn).to_be_enabled(timeout=timeout)
        close_btn.click()

    def get_row_by_name(self, name: str):
        """row-id 기준으로 row 찾기"""
        return self.page.locator(f'div[role="row"][row-id="{name}"]').first

    def open_row_menu(self, kp_name: str, timeout: int = 10000):
        """특정 Key Pair row 의 '…'(dropdown) 메뉴 버튼 클릭"""
        row = self.get_row_by_name(kp_name)
        expect(row).to_be_visible(timeout=timeout)

        menu_btn = row.locator('button[data-slot="dropdown-menu-trigger"]').first
        expect(menu_btn).to_be_enabled(timeout=timeout)
        menu_btn.click()

    def click_delete_in_menu(self, timeout: int = 10000):
        """dropdown 메뉴에서 '삭제' 항목 클릭"""
        delete_item = self.page.get_by_role("menuitem", name="삭제")
        expect(delete_item).to_be_visible(timeout=timeout)
        delete_item.click()

    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_kp(self) -> str:
        """Key Pair 생성 플로우"""
        kp_name = generate_name("QA-KEY-", letters_only=True)

        self.open_create_modal(C.KP_CREATE)
        self.name_input.fill(kp_name)
        self.click_confirm_button()
        self.click_close_button()

        return kp_name

    def delete_kp(self, kp_name: str):
        """Key Pair 삭제 플로우"""
        self.open_row_menu(kp_name)
        self.click_delete_in_menu()
        self.run_delete_flow()