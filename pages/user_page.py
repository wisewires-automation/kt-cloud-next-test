""" 사용자 POM """

import time
import json
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_DIR = Path(__file__).resolve().parent
LOCATORS = json.loads((BASE_DIR / "locators.json").read_text(encoding="utf-8"))

class UserPage:

    ADMIN_BUTTON_NAME = LOCATORS["ADMIN_BUTTON_NAME"]
    USER_CREATE_BUTTON_NAME = LOCATORS["USER_CREATE_BUTTON_NAME"]

    ID_INPUT_PLACEHOLDER = LOCATORS["ID_INPUT_PLACEHOLDER"]                # 사용자 아이디
    NAME_INPUT_PLACEHOLDER = LOCATORS["NAME_INPUT_PLACEHOLDER"]               # 사용자 이름
    EMAIL_INPUT_PLACEHOLDER = LOCATORS["EMAIL_INPUT_PLACEHOLDER"]              # 이메일
    PHONE_INPUT_PLACEHOLDER = LOCATORS["PHONE_INPUT_PLACEHOLDER"]              # 휴대폰 번호
    PW_INPUT_PLACEHOLDER = LOCATORS["PW_INPUT_PLACEHOLDER"]                # 비밀번호
    PW_CONFIRM_INPUT_PLACEHOLDER = LOCATORS["PW_CONFIRM_INPUT_PLACEHOLDER"]        # 비밀번호 확인

    CONFIRM_BUTTON_NAME = LOCATORS["CONFIRM_BUTTON_NAME"]
    CREATE_SUCCESS_TEXT = LOCATORS["CREATE_SUCCESS_TEXT"]
    CREATE_FAIL_TEXT = LOCATORS["CREATE_FAIL_TEXT"]

    def __init__(self, page: Page):
        self.page = page

        self.admin_button = page.get_by_role("button", name=self.ADMIN_BUTTON_NAME, exact=True)
        self.create_user_button = (page.locator("button").filter(has_text=self.USER_CREATE_BUTTON_NAME).first)

        self.id_input = page.get_by_placeholder(self.ID_INPUT_PLACEHOLDER)
        self.name_input = page.get_by_placeholder(self.NAME_INPUT_PLACEHOLDER)
        self.email_input = page.get_by_placeholder(self.EMAIL_INPUT_PLACEHOLDER)
        self.phone_input = page.get_by_placeholder(self.PHONE_INPUT_PLACEHOLDER)
        self.pw_input = page.get_by_placeholder(self.PW_INPUT_PLACEHOLDER)
        self.pw_confirm_input = page.get_by_placeholder(self.PW_CONFIRM_INPUT_PLACEHOLDER)
        
        self.switch_label = page.locator('label.s-switch__root__label[data-testid="s-switch-label"]')

        self.confirm_button = page.get_by_role("button",name=self.CONFIRM_BUTTON_NAME)

    # ===== 공통 동작 =====
    def go_manage_admin(self, timeout: int = 10000):
        expect(self.admin_button).to_be_visible(timeout=timeout)
        self.admin_button.click()

    def click_create_user_button(self, timeout: int = 10000):
        expect(self.create_user_button).to_be_visible(timeout=timeout)
        self.create_user_button.click()

    def fill_form(self, id: str, name: str, email: str, phone: str):
        self.id_input.fill(id)
        self.name_input.fill(name)
        self.email_input.fill(email)
        self.phone_input.fill(phone)

    def fill_pw_input(self, password: str):
        # 비밀번호 자동 생성 스위치 off
        self.switch_label.first.click()

        self.pw_input.fill(password)
        self.pw_confirm_input.fill(password)

    def submit(self, timeout: int = 20000):
        expect(self.confirm_button).to_be_visible(timeout=timeout)
        self.confirm_button.click()

        success_toast = self.page.get_by_text(self.CREATE_SUCCESS_TEXT)
        fail_toast = self.page.get_by_text(self.CREATE_FAIL_TEXT)
        
        try:
            expect(success_toast).to_be_visible(timeout=timeout)
        except Exception:
            try:
                expect(fail_toast).to_be_visible(timeout=timeout)
                raise AssertionError("사용자 생성 실패")
            except Exception:
                raise
    
    def create_user(self, id: str, name: str, email: str, phone: str, password: str) -> str:
        self.click_create_user_button()
        time.sleep(3)
        self.fill_form(id, name, email, phone)
        time.sleep(3)
        self.fill_pw_input(password)
        time.sleep(3)
        self.submit()
        time.sleep(3)

    
