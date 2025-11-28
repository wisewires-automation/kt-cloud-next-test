""" User POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.actions import CreateButtonLocators as C

class UserPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    ID_INPUT_PLACEHOLDER = '사용자 아이디를 입력해주세요.'            # 사용자 아이디 입력 필드 placeholder
    NAME_INPUT_PLACEHOLDER = '사용자 이름을 입력해주세요.'            # 사용자 이름 입력 필드placeholder
    EMAIL_INPUT_PLACEHOLDER = '이메일을 입력해주세요.'               # 이메일 입력 필드placeholder
    PHONE_INPUT_PLACEHOLDER = "'-'를 제외하고 숫자만 입력해주세요."   # 휴대폰 번호 입력 필드placeholder
    PW_INPUT_PLACEHOLDER = '비밀번호를 입력해주세요.'                # 비밀번호 입력 필드placeholder
    PW_CONFIRM_INPUT_PLACEHOLDER = '비밀번호를 확인해주세요.'        # 비밀번호 확인 입력 필드placeholder
    EDIT_EMAIL_INPUT_PLACEHOLDER = "사용자 ID로 사용할 이메일을 입력하세요."

    ROLE_EDIT_BUTTON_NAME = "역할 수정"
    ORG_ROLE_TEXT = "조직 역할"
    PROJECT_ROLE_TEXT = "프로젝트 역할"
    ASSIGN_BUTTON_NAME = "역할 할당"

    CONFIRM_BUTTON_NAME = "확인"
    CREATE_SUCCESS_TEXT = "생성 완료"
    CREATE_FAIL_TEXT = "생성 실패"

    DELETE_USER_TEXT = "사용자 삭제"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    # ============================================================
    # PROPERTIES
    # ============================================================
    @property
    def id_input(self):
        """사용자 아이디 입력 필드"""
        return self.page.get_by_placeholder(self.ID_INPUT_PLACEHOLDER)

    @property
    def name_input(self):
        """사용자 이름 입력 필드"""
        return self.page.get_by_placeholder(self.NAME_INPUT_PLACEHOLDER)
    
    @property
    def email_input(self):
        """사용자 이메일 입력 필드"""
        return self.page.get_by_placeholder(self.EMAIL_INPUT_PLACEHOLDER)
    
    @property
    def edit_email_input(self):
        """사용자 이메일 입력 필드(수정시)"""
        return self.page.get_by_placeholder(self.EDIT_EMAIL_INPUT_PLACEHOLDER)
    
    @property
    def phone_input(self):
        """사용자 휴대폰 번호 입력필드"""
        return self.page.get_by_placeholder(self.PHONE_INPUT_PLACEHOLDER)
    
    @property
    def pw_input(self):
        """사용자 비밀번호 입력 필드"""
        return self.page.get_by_placeholder(self.PW_INPUT_PLACEHOLDER)
    
    @property
    def pw_confirm_input(self):
        """사용자 비밀번호 확인 입력 필드"""
        return self.page.get_by_placeholder(self.PW_CONFIRM_INPUT_PLACEHOLDER)
    
    @property
    def switch_label(self):
        """비밀번호 자동생성 토글"""
        return self.page.locator('label.s-switch__root__label[data-testid="s-switch-label"]')
    
    @property
    def delete_user_button(self):
        """사용자 삭제 버튼"""
        return self.page.get_by_role("button", name=self.DELETE_USER_TEXT, exact=True)
    
    @property
    def row(self):
        return self.page.locator("div[role='row']")
    
    @property
    def login_id_cell(self):
        return "div[role='gridcell'][col-id='loginId'] .s-data-grid__default-cell"
    
    @property
    def role_name_cell(self):
        return "div[role='gridcell'][col-id='roleName'] .s-data-grid__default-cell"

    @property
    def role_edit_button(self):
        return self.page.get_by_role("button", name=self.ROLE_EDIT_BUTTON_NAME)
    
    @property
    def role_assign_button(self):
        return self.page.get_by_role("button", name=self.ASSIGN_BUTTON_NAME)

    @property
    def radio_group(self):
        return self.page.locator('label[data-testid="radio-label"]')
    
    @property
    def org_role_radio(self):
        return self.radio_group.filter(has_text=self.ORG_ROLE_TEXT)

    @property
    def project_role_radio(self):
        return self.radio_group.filter(has_text=self.PROJECT_ROLE_TEXT)

    # ============================================================
    # ACTIONS
    # ============================================================
    def enter_id(self, id):
        """사용자 아이디 입력"""
        self.id_input.fill(id)

    def enter_name(self, name):
        """사용자 비밀번호 입력"""
        self.name_input.fill(name)

    def enter_email(self, email):
        """사용자 이메일 입력"""
        self.email_input.fill(email)

    def enter_email_edit(self, email):
        """사용자 이메일 입력"""
        self.edit_email_input.fill(email)

    def enter_phone(self, phone):
        """사용자 휴대폰번호  입력"""
        self.phone_input.fill(phone)

    def fill_pw_form(self, password: str):
        """사용자 비밀번호/비밀번호 확인 입력"""
        # 비밀번호 자동 생성 스위치 off
        self.switch_label.first.click()

        self.pw_input.fill(password)
        self.pw_confirm_input.fill(password)
    
    def click_delete_user(self, timeout: int = 10000):
        """사용자 삭제 버튼 클릭"""
        btn = self.page.get_by_role("button", name=self.DELETE_USER_TEXT).first
        expect(btn).to_be_attached(timeout=timeout)
        btn.evaluate("el => el.click()")

    def click_user_row(self, id: str, timeout: int = 10000):
        """id와 일치하는 row 클릭"""
        user_row = self.row.filter(has=self.page.locator(self.login_id_cell, has_text=id)).first
        expect(user_row).to_be_visible(timeout=timeout)
        user_row.click()

    def click_role_edit(self, timeout: int = 10000):
        """역할 수정 버튼 클릭"""
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
    
    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_user(self, id: str, name: str, email: str, phone: str, password: str):
        """사용자 생성 플로우"""
        self.open_create_modal(C.USER_CREATE)
        self.enter_id(id)
        self.enter_name(name)
        self.enter_email(email)
        self.enter_phone(phone)
        self.fill_pw_form(password)
        self.click_button()

    def update_user_info(self, user_id: str, name: str, email: str, phone: str):
        """사용자 수정 플로우"""
        self.click_user_row(id=user_id)
        self.click_button(text="수정")
        self.enter_name(name)
        self.enter_email_edit(email)
        self.enter_phone(phone)
        self.click_button()

    def update_user_password(self, user_id: str, password: str):
        """사용자 비밀번호 변경 플로우"""
        self.click_user_row(id=user_id)
        self.click_button(text="비밀번호 변경")
        self.fill_pw_form(password)
        self.click_button()

    def delete_user(self, user_id: str):
        """사용자 삭제 플로우"""
        self.click_user_row(id=user_id)
        self.click_delete_user()
        self.run_delete_flow()


    
