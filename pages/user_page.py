""" User POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.locators.actions import SidebarLocators as S

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

    # ============================================================
    # ACTIONS
    # ============================================================
    def fill_form(self, id: str, name: str, email: str, phone: str):
        """사용자 아이디, 비밀번호, 이메일, 비밀번호"""
        self.id_input.fill(id)
        self.name_input.fill(name)
        self.email_input.fill(email)
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
    
    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_user(self, id: str, name: str, email: str, phone: str, password: str) -> str:
        """사용자 생성 플로우"""
        self.fill_form(id, name, email, phone)
        self.fill_pw_form(password)
        self.submit()



    
