""" 역할 POM """

from playwright.sync_api import Page, expect

class RolePage:

    # ===== selector / text 상수 =====
    ROLE_EDIT_BUTTON_NAME = "역할 수정"

    ORG_ROLE_TEXT = "조직 역할"
    PROJECT_ROLE_TEXT = "프로젝트 역할"

    ASSIGN_BUTTON_NAME = "역할 할당"

    def __init__(self, page: Page):
        self.page = page

        self.row = page.locator("div[role='row']")
        self.login_id_cell = "div[role='gridcell'][col-id='loginId'] .s-data-grid__default-cell"
        self.role_name_cell = "div[role='gridcell'][col-id='roleName'] .s-data-grid__default-cell"

        self.role_edit_button = page.get_by_role("button", name=self.ROLE_EDIT_BUTTON_NAME)
        self.role_assign_button = page.get_by_role("button", name=self.ASSIGN_BUTTON_NAME)

        self.radio_group = page.locator('label[data-testid="radio-label"]')
        self.org_role_radio = self.radio_group.filter(has_text=self.ORG_ROLE_TEXT)
        self.project_role_radio = self.radio_group.filter(has_text=self.PROJECT_ROLE_TEXT)


    # ===== 공통 동작 =====
    def click_user_row(self, id: str, timeout: int = 10000):
        # id와 일치하는 row 클릭
        user_row = self.row.filter(has=self.page.locator(self.login_id_cell, has_text=id))
        expect(user_row).to_be_visible(timeout=timeout)
        user_row.click()

    def click_role_edit(self, timeout: int = 10000):
        # 역할 할당 버튼 클릭
        expect(self.role_edit_button).to_be_visible(timeout=timeout)
        self.role_edit_button.click()

    def click_radio_group(self, is_org: bool = True):
        if (is_org):
            self.org_role_radio.click()
        else:
            self.project_role_radio.click()

    def click_role_assign(self, timeout: int = 10000):
        # 역할 할당 버튼 클릭
        expect(self.role_assign_button).to_be_visible(timeout=timeout)
        self.role_assign_button.click()

    def click_role_checkbox_by_name(self, role_name: str, timeout: int = 10000):
        role_row = self.row.filter(has=self.page.locator(self.role_name_cell, has_text=role_name))
        expect(role_row).to_be_visible(timeout=timeout)

        checkbox = role_row.locator("div[role='gridcell'][col-id='1'] input[type='checkbox']")
        expect(checkbox).to_be_visible(timeout=timeout)
        checkbox.click()
    
