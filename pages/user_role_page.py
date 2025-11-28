""" User POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.common import ButtonLocators as B

class UserRolePage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    ROLE_EDIT_TEXT = "역할 수정"        # 역할 수정 버튼 텍스트
    ROLE_ASSIGN_TEXT = "역할 할당"      # 역할 할당 버튼 텍스트

    ORG_ROLE_TEXT = "조직 역할"
    PROJECT_ROLE_TEXT = "프로젝트 역할"

    PROJECT_SELECT_NAME = "프로젝트 선택" # 프로젝트 선택 셀렉트박스 placeholder

    ASSIGNABLE_ROLE_SECTION = "할당 가능한 역할 목록"
    ASSIGNED_ROLE_SECTION = "할당된 역할 목록"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    # ============================================================
    # PROPERTIES
    # ============================================================
    @property
    def role_edit_button(self):
        """역할 수정 버튼 locator"""
        return self.page.get_by_role("button", name=self.ROLE_EDIT_TEXT)
    
    @property
    def role_assign_button(self):
        """역할 할당 버튼 locator"""
        return self.page.get_by_role("button", name=self.ROLE_ASSIGN_TEXT)

    @property
    def radio_group(self):
        """역할 선택 라디오 locator"""
        return self.page.locator('label[data-testid="radio-label"]')
    
    @property
    def org_role_radio(self):
        """조직 역할 라디오 locator"""
        return self.radio_group.filter(has_text=self.ORG_ROLE_TEXT)

    @property
    def project_role_radio(self):
        """프로젝트 역할 라디오 locator"""
        return self.radio_group.filter(has_text=self.PROJECT_ROLE_TEXT)
    
    @property
    def project_select(self):
        """프로젝트 선택용 selectbox locator"""
        return self.page.get_by_role("combobox").filter(has_text=self.PROJECT_SELECT_NAME).first


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

    def _get_row_in_section(self, section_title: str,role_name: str,timeout: int = 10000):
        """특정 섹션(할당 가능한/할당된 역할 목록)에 role_name의 row를 반환"""
        grid = self._get_grid_in_section(section_title)

        # roleName 셀 찾기
        role_cell = grid.locator(
            "div[role='gridcell'][col-id='roleName'] .s-data-grid__default-cell"
        ).filter(has_text=role_name).first

        expect(role_cell).to_be_visible(timeout=timeout)

        # 셀이 포함된 row 로 올라가기
        row = role_cell.locator("xpath=ancestor::div[@role='row']").first
        expect(row).to_be_visible(timeout=timeout)

        return row
    
    # ============================================================
    # ACTIONS
    # ============================================================
    def click_role_edit(self, timeout: int = 10000):
        """역할 수정 버튼 클릭"""
        btn = self.role_edit_button
        expect(btn).to_be_visible(timeout=timeout)
        btn.click()

    def select_role(self, is_org: bool = True):
        """역할 선택 (default: 조직 역할)"""
        if (is_org):
            self.org_role_radio.click()
        else:
            self.project_role_radio.click()

    def click_role_assign(self, timeout: int = 10000):
        """역할 할당 버튼 클릭"""
        btn = self.role_assign_button
        expect(btn).to_be_visible(timeout=timeout)
        btn.click()

    def check_role_by_name(self, role_name: str = "USER_MANAGER", timeout: int = 10000):
        """역할 체크박스 선택"""
        row = self._get_row_in_section(
            section_title=self.ASSIGNABLE_ROLE_SECTION,
            role_name=role_name,
            timeout=timeout
        )

        # row 안의 체크박스
        checkbox_label = row.locator("label.s-checkbox").first
        expect(checkbox_label).to_be_visible(timeout=timeout)
        checkbox_label.click()

    def select_project_by_name(self, project_name: str, timeout: int = 10000):
        """프로젝트 이름으로 프로젝트 선택"""
        self.project_select.click()

        option = self.page.get_by_role("option", name=project_name)
        expect(option).to_be_visible(timeout=timeout)
        option.click()

    def click_role_delete(self, role_name: str, timeout: int = 10000):
        """역할 삭제 버튼 클릭"""
        row = self._get_row_in_section(
            section_title=self.ASSIGNED_ROLE_SECTION,
            role_name=role_name,
            timeout=timeout,
        )
        delete_btn = row.get_by_role("button", name=B.DELETE_TEXT).first
        expect(delete_btn).to_be_enabled(timeout=timeout)
        delete_btn.click()

    # ===== 테스트 시나리오 단위 ACTIONS =====
    def assign_org_roles(self, roles: list[str]):
        """조직 역할 할당 플로우"""
        for role in roles:
            self.check_role_by_name(role_name=role)

        self.click_role_assign()

        # 성공메세지 - 00개의 역할을 성공적으로 할당되었습니다.

    def assign_project_roles(self, project_name: str, roles: list[str]):
        """프로젝트 역할 할당 플로우"""
        self.select_role(is_org=False)
        self.select_project_by_name(project_name=project_name)

        for role in roles:
            self.check_role_by_name(role_name=role)

        self.click_role_assign()

        # 성공메세지 - 00개의 역할을 성공적으로 할당되었습니다.

    def unassign_role(self, roles: list[str]):
        """역할 해제 플로우"""
        for role in roles:
            self.click_role_delete(role_name=role)

        # 성공메세지 - 역할이 성공적으로 해제되었습니다.





    
