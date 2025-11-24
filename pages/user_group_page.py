""" User POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.locators.actions import SidebarLocators as S

class UserGroupPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    NAME_INPUT = 'input[name="name"]'                       # 사용자 그룹 이릅 입력 필드
    DESC_INPUT = 'input[name="description"]'                # 사용자 그룹 설명 입력 필드

    DELETE_USER_GROUP_TEXT = "사용자 그룹 삭제"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    # ============================================================
    # PROPERTIES
    # ============================================================
    @property
    def user_group_menu(self):
        """사용자 그룹 메뉴"""
        return self.page.locator(".s-vertical-navigation-menu-item__container").filter(has_text=S.USER_GROUP_MENU)
    
    @property
    def name_input(self):
        """사용자 그룹 이름 입력 필드"""
        return self.page.locator(self.NAME_INPUT)

    @property
    def desc_input(self):
        """사용자 그룹 설명 입력 필드"""
        return self.page.locator(self.DESC_INPUT)
    
    @property
    def delete_user_button(self):
        """사용자 삭제 버튼"""
        return self.page.get_by_role("button", name=self.DELETE_USER_GROUP_TEXT, exact=True)
    
    @property
    def row(self):
        return self.page.locator("div[role='row']")
    
    @property
    def name_cell(self):
        return  "div[role='gridcell'][col-id='name'] .s-data-grid__default-cell"

    # ============================================================
    # ACTIONS
    # ============================================================
    def go_user_group_menu(self, timeout: int = 10000):
        expect(self.user_group_menu).to_be_visible(timeout=timeout)
        self.user_group_menu.click()

    def fill_form(self, name: str, desc: str):
        """사용자 그룹 이름/설명 입력"""
        self.name_input.fill(name)
        self.desc_input.fill(desc)

    def click_delete_user_group(self, timeout: int = 10000):
        """사용자 그룹 삭제 버튼 클릭"""
        btn = self.page.get_by_role("button", name=self.DELETE_USER_GROUP_TEXT).first
        expect(btn).to_be_attached(timeout=timeout)
        btn.evaluate("el => el.click()")
    
    def click_user_row(self, name: str, timeout: int = 10000):
        user_row = self.row.filter(has=self.page.locator(self.name_cell, has_text=name))
        expect(user_row).to_be_visible(timeout=timeout)
        user_row.click()

    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_user_group(self, name: str, desc: str):
        """사용자 생성 플로우"""
        self.fill_form(name, desc)
        self.submit()



    
