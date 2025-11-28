""" 로그인, 로그아웃 POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.common import ToastLocators as T, ButtonLocators as B

class AuthPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    ORG_CODE_INPUT = 'input[name="orgCode"]'    # IAM 조직 아이디 입력 필드
    USERNAME_INPUT = 'input[name="username"]'   # 로그인 아이디 입력 필드
    PASSWORD_INPUT = 'input[name="password"]'   # 로그인 비밀번호 입력 필드

    LOGIN_BUTTON_NAME = "로그인"
    LOGIN_SUCCESS_TEXT = "로그인 성공"

    KT_TAB_NAME = "kt cloud 계정"                 # KT Cloud 계정 탭 이름
    IAM_TAB_NAME = "IAM 계정"                     # IAM 계정 탭 이름

    USER_IMG_NAME = "user"                       # 우측 상단 사용자 아이콘
    LOGOUT_MENU_TEXT = "로그아웃"
    LOGOUT_CONFIRM_TEXT = "로그아웃 하시겠습니까?"
    LOGOUT_CONFIRM_BUTTON_NAME = "확인"
    LOGOUT_SUCCESS_TEXT = "로그아웃 성공"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    # ============================================================
    # PROPERTIES
    # ============================================================
    @property
    def org_code_input(self):
        """IAM 계정 로그인 - 그룹 아이디 입력 필드 locator"""
        return self.page.locator(self.ORG_CODE_INPUT)

    @property
    def username_input(self):
        """로그인 아이디 입력 필드 locator"""
        return self.page.locator(self.USERNAME_INPUT)

    @property
    def password_input(self):
        """로그인 비밀번호 입력 필드 locator"""
        return self.page.locator(self.PASSWORD_INPUT)

    @property
    def login_button(self):
        """로그인 버튼 locator"""
        return self.page.get_by_role("button", name=self.LOGIN_BUTTON_NAME)

    @property
    def user_img(self):
        """우측 상단 사용자 이미지 아이콘 locator"""
        return self.page.get_by_role("img", name=self.USER_IMG_NAME).first

    @property
    def logout_menu(self):
        """사용자 드롭다운 메뉴 내 '로그아웃' 항목 locator"""
        return self.page.get_by_text(self.LOGOUT_MENU_TEXT)

    @property
    def logout_confirm_text(self):
        """로그아웃 확인 모달 본문 텍스트 locator"""
        return self.page.get_by_text(self.LOGOUT_CONFIRM_TEXT)

    @property
    def logout_confirm_button(self):
        """로그아웃 확인 모달의 '확인' 버튼 locator"""
        return self.page.get_by_role("button", name=self.LOGOUT_CONFIRM_BUTTON_NAME)

    # ============================================================
    # ACTIONS
    # ============================================================
    def goto(self, url: str):
        """로그인 페이지 이동 및 페이지가 준비될 때까지 대기"""
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")
        expect(self.username_input).to_be_visible(timeout=10000)

    def click_tab(self, tab_name: str):
        """로그인 탭 선택 (KT / IAM)"""
        self.page.get_by_role("tab", name=tab_name).click()

    def enter_group_id(self, group_id: str):
        """IAM 계정 로그인 - 그룹(조직) 아이디 입력"""
        self.org_code_input.fill(group_id)

    def enter_id(self, user_id: str):
        """로그인 아이디 입력"""
        self.username_input.fill(user_id)

    def enter_password(self, user_pw: str):
        """로그인 비밀번호 입력"""
        self.password_input.fill(user_pw)

    def click_login(self):
        """로그인 버튼 클릭"""
        expect(self.login_button).to_be_enabled(timeout=10000)
        self.login_button.click()

    def wait_login_success(self, timeout: int = 10000):
        """로그인 성공 토스트 메시지 검증"""
        expect(
            self.page.get_by_text(self.LOGIN_SUCCESS_TEXT, exact=True)
        ).to_be_visible(timeout=timeout)

    # ===== 테스트 시나리오 단위 ACTIONS =====
    def login_admin(self, url: str, user_id: str, user_pw: str):
        """
        KT Cloud 계정 로그인 플로우

        1) 로그인 페이지 이동
        2) 아이디/비밀번호 입력
        3) 로그인 버튼 클릭
        4) 로그인 성공 확인
        """
        self.goto(url)
        self.enter_id(user_id)
        self.enter_password(user_pw)
        self.click_login()
        self.wait_login_success()

    def login_iam(self, url: str, group_id: str, user_id: str, user_pw: str):
        """
        IAM 계정 로그인 플로우

        1) 로그인 페이지 이동
        2) IAM 계정 탭 클릭
        3) 그룹 아이디/아이디/비밀번호 입력
        4) 로그인 버튼 클릭
        5) 로그인 성공 확인
        """
        self.goto(url)
        self.click_tab(self.IAM_TAB_NAME)
        self.enter_group_id(group_id)
        self.enter_id(user_id)
        self.enter_password(user_pw)
        self.click_login()
        self.wait_login_success()

    def logout(self, timeout: int = 10000):
        """로그아웃 플로우"""
        self.user_img.click()
        self.logout_menu.click()
        expect(self.logout_confirm_text).to_be_visible(timeout=timeout)
        self.logout_confirm_button.click()
        expect(
            self.page.get_by_text(self.LOGOUT_SUCCESS_TEXT, exact=True)
        ).to_be_visible(timeout=timeout)
