""" NAT Gateway POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.locators.common import ToastLocators as T, ButtonLocators as B
from utils.namer import make_name

class NATPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    NAME_INPUT = 'input[name="name"]'          # NAT Gateway 이름
    VPC_SELECT_NAME = "VPC를 선택하세요"         # VPC 선택 Placeholder

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self.vpc_select = (self.page.get_by_role("combobox").filter(has_text=self.VPC_SELECT_NAME).first)
        self.vpc_label = self.page.locator("label.s-select-radio-label")
        self.vpc_option = self.page.locator(".s-select-options-container .s-select-item--option")

        self.confirm_button = page.get_by_role("button", name=B.CREATE_BUTTON_NAME)

    # ============================================================
    # PROPERTIES (locator 객체를 반환)
    # ============================================================ 
    @property
    def name_input(self):
        """모달 - NAT Gateway 이름 입력 필드"""
        return self.page.locator(self.NAME_INPUT)

    # ============================================================
    # ACTIONS
    # ============================================================
    def open_rt_create(self, timeout: int = 10000):
        expect(self.rt_nav_button).to_be_visible(timeout=timeout)
        self.rt_nav_button.click()

        expect(self.rt_create_button).to_be_visible(timeout=timeout)
        self.rt_create_button.click()

    def fill_form(self, name: str, desc: str):
        self.name_input.fill(name)

    def select_vpc_by_name(self, vpc_name: str, timeout: int = 10000):
        self.vpc_select.click()
        vpc_label = self.vpc_label.filter(has_text=vpc_name).first

        expect(vpc_label).to_be_visible(timeout=timeout)
        vpc_label.click()

    def select_first_vpc(self):
        self.vpc_select.click()
        self.vpc_option.nth(0).click()

    def submit(self, timeout: int = 10000):
        expect(self.confirm_button).to_be_enabled(timeout=timeout)
        self.confirm_button.click()

        success_toast = self.page.get_by_text(T.CREATE_SUCCESS_TEXT)
        fail_toast = self.page.get_by_text(T.CREATE_FAIL_TEXT)
        
        try:
            expect(success_toast).to_be_visible(timeout=timeout)
        except Exception:
            try:
                expect(fail_toast).to_be_visible(timeout=timeout)
                raise AssertionError("Nat Gateway 생성 실패")
            except Exception:
                raise

    def create_nat(self, name_prefix: str = "NAT-", desc: str = "", vpc_name: str = "") -> str:
        nat_name = make_name(prefix="QA-NAT-")

        # vpc 명이 있을 경우 이름으로 선택 없을 경우 제일 첫번째 옵션 선택
        if vpc_name:
            self.select_vpc_by_name(vpc_name)
        else:
            self.select_first_vpc()

        self.fill_form(name=nat_name, desc=desc)
        self.submit()
        
        return nat_name