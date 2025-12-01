"""Snapshot POM """

from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.actions import SidebarLocators as S, CreateButtonLocators as C

class SnapPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    # ============================================================
    # PROPERTIES
    # ============================================================ 


    # ============================================================
    # ACTIONS
    # ============================================================

    # ===== 테스트 시나리오 단위 ACTIONS =====
    def update_snap(self, snap_name: str, new_name: str):
        """Snapshot 수정 플로우"""
        self.go_link_by_name(name=snap_name)
        self.run_rename_flow(new_name=new_name)
    
    def delete_snap(self, snap_name: str):
        """Snapshot 삭제 플로우"""
        self.go_link_by_name(name=snap_name)
        self.open_delete_modal()
        self.run_delete_flow()