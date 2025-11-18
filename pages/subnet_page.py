""" Subnet POM """

from playwright.sync_api import Page, expect
from utils.namer import make_name

class SubnetPage:

    # ===== selector / text 상수 =====
    SUBNET_NAV_BUTTON_NAME = "Subnet"
    SUBNET_CREATE_BUTTON_NAME = "Subnet 생성"

    VPC_SELECT_NAME = "VPC를 선택해주세요"         # VPC 선택 Placeholder

    SUBNET_NAME_INPUT = 'input[name="name"]'    # Subnet 이름
    SUBNET_CIDR_INPUT = 'input[name="cidr"]'    # Subnet CIDR 블록

    CONFIRM_BUTTON_NAME = "확인"
    
    CREATE_SUCCESS_TEXT = "Subnet 생성 성공"
    CREATE_FAIL_TEXT = "생성 실패"

    def __init__(self, page: Page):
        self.page = page

        self.subnet_nav_button = page.get_by_role("button", name=self.SUBNET_NAV_BUTTON_NAME, exact=True)
        self.subnet_create_button = (page.locator("button").filter(has_text=self.SUBNET_CREATE_BUTTON_NAME).first)

        self.name_input = page.locator(self.SUBNET_NAME_INPUT)
        self.cidr_input = page.locator(self.SUBNET_CIDR_INPUT)
        self.vpc_select = (self.page.get_by_role("combobox").filter(has_text=self.VPC_SELECT_NAME).first)
        self.vpc_label = self.page.locator("label.s-select-radio-label")
        self.vpc_option = self.page.locator(".s-select-options-container .s-select-item--option")

        self.confirm_button = page.get_by_role("button", name=self.CONFIRM_BUTTON_NAME)

    # ===== 공통 동작 =====
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
        fail_toast = self.page.get_by_text(self.CREATE_FAIL_TEXT)
        
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