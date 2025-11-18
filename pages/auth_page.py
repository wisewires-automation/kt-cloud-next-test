""" 로그인, 로그아웃 POM """

from playwright.sync_api import Page, expect

class AuthPage:

    # ===== selector / text 상수 =====
    ORG_CODE_INPUT = 'input[name="orgCode"]'    # 조직 아이디
    USERNAME_INPUT = 'input[name="username"]'   # 아이디
    PASSWORD_INPUT = 'input[name="password"]'   # 비밀번호

    LOGIN_BUTTON_NAME = "로그인"
    LOGIN_SUCCESS_TEXT = "로그인 성공"

    KT_TAB_NAME = "kt cloud 계정"
    IAM_TAB_NAME = "IAM 계정"

    USER_IMG_NAME = "user"
    LOGOUT_MENU_TEXT = "로그아웃"
    LOGOUT_CONFIRM_TEXT = "로그아웃 하시겠습니까?"
    LOGOUT_CONFIRM_BUTTON_NAME = "확인"
    LOGOUT_SUCCESS_TEXT = "로그아웃 성공"

    def __init__(self, page: Page):
        self.page = page

        # locator
        self.group_id_input = page.locator(self.ORG_CODE_INPUT)
        self.username_input = page.locator(self.USERNAME_INPUT)
        self.password_input = page.locator(self.PASSWORD_INPUT)
        self.login_button = page.get_by_role("button", name=self.LOGIN_BUTTON_NAME)

        # logout 관련
        self.user_img = page.get_by_role("img", name=self.USER_IMG_NAME).first
        self.logout_menu = page.get_by_text(self.LOGOUT_MENU_TEXT)
        self.logout_confirm_text = page.get_by_text(self.LOGOUT_CONFIRM_TEXT)
        self.logout_confirm_button = page.get_by_role("button", name=self.LOGOUT_CONFIRM_BUTTON_NAME)

    # ===== 공통 동작 =====
    def goto(self, url: str):
        self.page.goto(url)

        """로그인 페이지가 준비될 때까지 대기 (아이디 필드 기준)"""
        self.page.wait_for_load_state("networkidle")
        expect(self.page.locator(self.USERNAME_INPUT)).to_be_visible(timeout=10000)

    def click_tab(self, tab_name):
        self.page.get_by_role("tab", name=tab_name).click()

    def enter_group_id(self, group_id: str):
        self.group_id_input.fill(group_id)

    def enter_id(self, id: str):
        self.username_input.fill(id)

    def enter_password(self, password: str):
        self.password_input.fill(password)

    def click_login(self):
        expect(self.login_button).to_be_enabled(timeout=10000)
        self.login_button.click()

    def wait_login_success(self, timeout: int = 10000):
        """로그인 성공 토스트 검증"""
        expect(self.page.get_by_text(self.LOGIN_SUCCESS_TEXT, exact=True)).to_be_visible(timeout=timeout)

    # ===== KT Cloud 계정 로그인 ======
    def login_kt(self, url: str, user_id: str, password: str):
        """
        1) 로그인 페이지 이동
        2) 아이디/비밀번호 입력
        3) 로그인 버튼 클릭
        4) 로그인 성공 확인
        """
        self.goto(url)
        self.enter_id(user_id)
        self.enter_password(password)
        self.click_login()
        self.wait_login_success()

    # ====== IAM 계정 로그인 ======
    def login_iam(self, url: str, group_id: str, user_id: str, password: str):
        """
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
        self.enter_password(password)
        self.click_login()
        self.wait_login_success()
    
    # ====== 로그아웃 ======
    def logout(self, timeout: int = 10000):
        self.user_img.click()
        self.logout_menu.click()
        expect(self.logout_confirm_text).to_be_visible(timeout=timeout)
        self.logout_confirm_button.click()
        expect(self.page.get_by_text(self.LOGOUT_SUCCESS_TEXT, exact=True)).to_be_visible(timeout=timeout)

    
