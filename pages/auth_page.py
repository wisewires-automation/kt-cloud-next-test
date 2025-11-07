"""
로그인 페이지
"""

from playwright.sync_api import Page
from playwright.sync_api import expect
import time

class AuthPage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str):
        self.page.goto(url)

    def click_kt_tab(self):
        self.page.get_by_role("tab", name="kt cloud 계정").click()

    def enter_email(self, email: str):
        self.page.get_by_test_id("text-input-container").get_by_role("textbox", name="input").fill(email)

    def enter_password(self, password: str, timeout: int = 10000):
        self.page.get_by_role("textbox", name="password-input").click()
        self.page.get_by_role("textbox", name="password-input").fill(password)

        # 로그인 버튼이 보일때 까지 대기
        expect(self.page.get_by_role("button", name="로그인")).to_be_visible(timeout=timeout)

    def click_login(self):
        self.page.get_by_role("button", name="로그인").click()

    def wait_login_success(self, timeout: int = 10000):
        # 로그인 성공 토스트 검증
        expect(self.page.get_by_text("로그인 성공", exact=True)).to_be_visible(timeout=timeout)

    # 로그인
    def login(self, url: str, email: str, password: str, timeout: int = 10000):
        """
        로그인 플로우: 페이지 이동 -> 이메일/비번 입력 -> 로그인 -> 성공 텍스트 확인
        """
        self.goto(url)
        self.click_kt_tab()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        self.wait_login_success(timeout=timeout)

    def logout(self, timeout: int = 10000):
        self.locator('[aria-label="user"]').click()
        self.page.get_by_text("로그아웃").click()
        expect(self.page.get_by_role("button", name="로그인")).to_be_visible(timeout=timeout)
