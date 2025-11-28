""" User Group POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.actions import SidebarLocators as S, CreateButtonLocators as C

class UserGroupPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    NAME_INPUT = 'input[name="name"]'                       # 사용자 그룹 이릅 입력 필드
    DESC_INPUT = 'input[name="description"]'                # 사용자 그룹 설명 입력 필드

    EDIT_MEMBER_TEXT = "멤버 수정"
    DELETE_USER_GROUP_TEXT = "사용자 그룹 삭제"

    ADD_MEMBER_TEXT = "사용자 추가"
    DELETE_MEMBER_TEXT = "사용자 삭제"

    ASSIGNABLE_USER_SECTION = "할당 가능한 사용자 목록"
    ASSIGNED_USER_SECTION = "할당된 사용자 목록"

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
    # PRIVATE HELPERS
    # ============================================================
    def _get_grid_in_section(self, section_title: str):
        """섹션 제목을 기준으로 바로 뒤에 오는 역할 그리드를 반환"""
        heading = self.page.get_by_role("heading", name=section_title, exact=True)
        expect(heading).to_be_visible(timeout=10000)

        grid = heading.locator("xpath=following::div[@data-testid='s-data-grid'][1]")
        expect(grid).to_be_visible(timeout=10000)
        return grid

    def _get_row_in_section(self, user_id: str, sec_type: str, timeout: int = 10000):
        """특정 섹션(할당 가능한/할당된 역할 목록)에 role_name의 row를 반환"""

        if (sec_type == "ADD"):
            grid = self._get_grid_in_section(self.ASSIGNABLE_USER_SECTION)

            # ID 셀 찾기
            cell = grid.locator(
                "div[role='gridcell'][col-id='id'] .s-data-grid__default-cell"
            ).filter(has_text=user_id).first
        else:
            grid = self._get_grid_in_section(self.ASSIGNED_USER_SECTION)

            # 사용자 아이디 셀 찾기
            cell = grid.locator(
                "div[role='gridcell'][col-id='memberId'] .s-data-grid__default-cell"
            ).filter(has_text=user_id).first
        
        expect(cell).to_be_visible(timeout=timeout)

        # 셀이 포함된 row 로 올라가기
        row = cell.locator("xpath=ancestor::div[@role='row']").first
        expect(row).to_be_visible(timeout=timeout)

        return row

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

    def check_checkbox_by_id(self, user_id: str, sec_type: str = "ADD", timeout: int = 10000):
        """row 체크박스 선택"""
        row = self._get_row_in_section(user_id, sec_type, timeout)

        # row 안의 체크박스
        checkbox_label = row.locator("label.s-checkbox").first
        expect(checkbox_label).to_be_visible(timeout=timeout)
        checkbox_label.click()

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

    def add_group_member(self, group_name: str, user_ids: list[str]):
        """사용자 그룹 멤버 수정 플로우"""
        self.click_user_row(name=group_name)
        self.click_button(self.EDIT_MEMBER_TEXT)

        for user_id in user_ids:
            self.check_checkbox_by_id(user_id, "ADD")

        self.click_button(self.ADD_MEMBER_TEXT)

        # 사용자 그룹 멤버 수정 성공

    def delete_group_member(self, group_name: str, user_ids: list[str]):
        """사용자 그룹 멤버 삭제 플로우"""
        self.click_user_row(name=group_name)
        self.click_button(self.EDIT_MEMBER_TEXT)

        for user_id in user_ids:
            self.check_checkbox_by_id(user_id, "DELETE")

        self.click_button(self.DELETE_MEMBER_TEXT)

        # 사용자 그룹 멤버 삭제 성공




    
