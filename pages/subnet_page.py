""" Subnet POM """

from playwright.sync_api import Page, expect
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.locators.common import ToastLocators as T, ButtonLocators as B
from utils.namer import make_name

class SubnetPage:

    VPC_SELECT_NAME = "VPC를 선택해주세요"         # VPC 선택 Placeholder
    NAME_INPUT = 'input[name="name"]'    # Subnet 이름
    CIDR_INPUT = 'input[name="cidr"]'    # Subnet CIDR 블록
    CREATE_SUCCESS_TEXT = "Subnet 생성 성공"

    def __init__(self, page: Page):
        self.page = page

        self.subnet_nav_button = page.get_by_role("button", name=S.SUBNET_MENU, exact=True)
        self.subnet_create_button = (page.locator("button").filter(has_text=C.SUBNET_CREATE).first)
        self.name_input = page.locator(self.NAME_INPUT)
        self.cidr_input = page.locator(self.CIDR_INPUT)
        self.vpc_select = (self.page.get_by_role("combobox").filter(has_text=self.VPC_SELECT_NAME).first)
        self.vpc_label = self.page.locator("label.s-select-radio-label")
        self.vpc_option = self.page.locator(".s-select-options-container .s-select-item--option")

        self.confirm_button = page.get_by_role("button", name=B.CONFIRM_BUTTON)

    def open_subnet_create(self, timeout: int = 10000):
        expect(self.subnet_nav_button).to_be_visible(timeout=timeout)
        self.subnet_nav_button.click()

        expect(self.subnet_create_button).to_be_visible(timeout=timeout)
        self.subnet_create_button.click()

    def select_vpc_by_name(self, vpc_name: str, timeout: int = 10000):
        self.vpc_select.click()
        vpc_label = self.vpc_label.filter(has_text=vpc_name).first

        expect(vpc_label).to_be_visible(timeout=timeout)
        vpc_label.click()

    def select_first_vpc(self):
        self.vpc_select.click()
        self.vpc_option.nth(0).click()

    def fill_form(self, name: str, cidr: str):
        self.name_input.fill(name)
        self.cidr_input.fill(cidr)

    def submit(self, timeout: int = 10000):
        expect(self.confirm_button).to_be_enabled(timeout=timeout)
        self.confirm_button.click()

        """Subnet 생성 토스트 검증"""
        success_toast = self.page.get_by_text(self.CREATE_SUCCESS_TEXT)
        fail_toast = self.page.get_by_text(T.CREATE_FAIL_TEXT)
        
        try:
            # 1차: 성공 토스트 대기
            expect(success_toast).to_be_visible(timeout=timeout)
        except Exception:
            # 2차: 실패 토스트 확인
            try:
                expect(fail_toast).to_be_visible(timeout=timeout)
                raise AssertionError("Subnet 생성 실패")
            except Exception:
                raise

    def create_subnet(self, name_prefix: str = "QA-SUB-", cidr: str = "10.0.0.0/8", vpc_name: str = "") -> str:
        subnet_name = make_name(prefix=name_prefix)

        # vpc 명이 있을 경우 이름으로 선택 없을 경우 pass
        if vpc_name:
            self.select_vpc_by_name(vpc_name)

        self.fill_form(name=subnet_name, cidr=cidr)
        self.submit()
        return subnet_name