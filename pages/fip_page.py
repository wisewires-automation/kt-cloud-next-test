""" Floating IP POM """

from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.locators.common import ButtonLocators as B
from pages.locators.actions import CreateButtonLocators as C

class FIPPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    CREATE_SUCCESS_TEXT = "Floating IP가 성공적으로 생성되었습니다."

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # ============================================================
    # ACTIONS
    # ============================================================
    def fill_form(self, name: str, desc: str):
        """네트워크 ACL 이름, 설명 입력"""
        self.name_input.fill(name)

        if desc is not None:
            self.desc_input.fill(desc)
        
    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_fip(self) -> str:
        """Floating IP 생성 플로우"""
        self.open_create_modal(C.FIP_CREATE)
        self.click_button(text=B.CREATE_TEXT)
    
    def delete_fip(self, fip_name: str):
        """Floating IP 삭제 플로우"""
        self.go_link_by_name(name=fip_name)
        self.open_delete_modal()
        self.run_delete_flow()