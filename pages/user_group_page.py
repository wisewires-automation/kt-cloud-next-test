""" User Group POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C

class UserGroupPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    NAME_INPUT = 'input[name="name"]'                       # 사용자 그룹 이릅 입력 필드
    DESC_INPUT = 'input[name="description"]'                # 사용자 그룹 설명 입력 필드

    EDIT_MEMBER_TEXT = "멤버 수정"
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

    # ============================================================
    # ACTIONS
    # ============================================================
    def go_user_group_menu(self, timeout: int = 10000):
        """사용자 그룹 메뉴로 이동"""
        expect(self.user_group_menu).to_be_visible(timeout=timeout)
        self.user_group_menu.click()

    def enter_name(self, name: str):
        """사용자 그룹 이름 입력"""
        self.name_input.fill(name)

    def enter_desc(self, desc: str):
        """사용자 그룹 이름 입력"""
        self.desc_input.fill(desc)

    def fill_form(self, name: str, desc: str):
        """사용자 폼 입력"""
        self.enter_name(name)
        self.enter_desc(desc)

    def click_user_row(self, name: str, timeout: int = 10000):
        """사용자 row 클릭"""
        row = self.page.locator("div[role='row']")
        name_cell = "div[role='gridcell'][col-id='name'] .s-data-grid__default-cell"
        user_row = row.filter(has=self.page.locator(name_cell, has_text=name))
        expect(user_row).to_be_visible(timeout=timeout)
        user_row.click()

    def click_delete_user_group(self, timeout: int = 10000):
        """사용자 그룹 삭제 버튼 클릭"""
        btn = self.page.get_by_role("button", name=self.DELETE_USER_GROUP_TEXT).first
        expect(btn).to_be_attached(timeout=timeout)
        btn.evaluate("el => el.click()")

    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_user_group(self, name: str, desc: str):
        """사용자 생성 플로우"""
        self.open_create_modal(C.USER_GROUP_CREATE)
        self.fill_form(name, desc)
        self.click_button()

    def delete_user_group(self, group_name: str):
        """사용자 그룹 삭제 플로우"""
        self.click_user_row(name=group_name)
        self.click_delete_user_group()
        self.run_delete_flow()



    
