""" Floating IP POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.common import ButtonLocators as B
from pages.actions import CreateButtonLocators as C

class FIPPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    CREATE_SUCCESS_TEXT = "Floating IP가 성공적으로 생성되었습니다."

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    # ============================================================
    # PROPERTIES
    # ============================================================ 
    @property
    def id_cell(self):
        """이름 셀"""
        return self.page.locator(".ag-pinned-left-cols-container [role='gridcell'][col-id='id']")

    # ============================================================
    # ACTIONS
    # ============================================================
    def go_link_by_id(self, name: str, timeout: int = 10000) -> None:
        """이름 링크 페이지로 이동"""
        cell = self.id_cell.filter(has_text=name).first
        expect(cell).to_be_visible(timeout=timeout)

        link = cell.locator("a").first
        expect(link).to_be_visible(timeout=timeout)

        link.click()

    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_fip(self) -> str:
        """Floating IP 생성 플로우"""
        self.open_create_modal(C.FIP_CREATE)
        self.click_button(text=B.CREATE_TEXT)
    
    def delete_fip(self, fip_name: str):
        """Floating IP 삭제 플로우"""
        self.go_link_by_id(name=fip_name)
        self.open_delete_modal()
        self.run_delete_flow()
        # 삭제 완료