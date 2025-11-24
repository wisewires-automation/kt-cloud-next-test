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
    NAME_INPUT = 'input[name="name"]'       # NAT Gateway 이름 입력 필드
    VPC_SELECT_NAME = "VPC를 선택하세요"      # VPC 선택 셀렉트박스 placeholder 텍스트

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    # ============================================================
    # PROPERTIES (locator 객체를 반환)
    # ============================================================ 
    @property
    def name_input(self):
        """NAT Gateway 생성 모달 - 이름 입력 필드 locator"""
        return self.page.locator(self.NAME_INPUT)
    
    @property
    def vpc_select(self):
        """NAT Gateway 생성 모달 - VPC 선택용 셀렉트박스 locator"""
        return self.page.get_by_role("combobox").filter(
            has_text=self.VPC_SELECT_NAME
        ).first

    @property
    def vpc_label(self):
        """NAT Gateway 생성 모달 - VPC 라디오 옵션의 label locator"""
        return self.page.locator("label.s-select-radio-label")

    @property
    def vpc_option(self):
        """NAT Gateway 생성 모달 - VPC 셀렉트 박스 옵션 locator"""
        return self.page.locator(".s-select-options-container .s-select-item--option")

    # ============================================================
    # ACTIONS
    # ============================================================
    def fill_form(self, name: str, desc: str):
        """NAT Gateway 생성 모달에 이름 입력"""
        self.name_input.fill(name)

    def select_vpc_by_name(self, vpc_name: str, timeout: int = 10000):
        """VPC 이름으로 VPC 선택"""
        self.vpc_select.click()
        vpc_label = self.vpc_label.filter(has_text=vpc_name).first

        expect(vpc_label).to_be_visible(timeout=timeout)
        vpc_label.click()

    def select_first_vpc(self):
        """첫 번째 VPC 선택"""
        self.vpc_select.click()
        self.vpc_option.nth(0).click()

    def create_nat(self, desc: str = "", vpc_name: str = "") -> str:
        """NAT Gateway 생성 플로우"""
        nat_name = make_name(prefix="QA-NAT-")

        # VPC 명이 있을 경우 해당 이름으로 선택, 없을 경우 첫 번째 옵션 선택
        if vpc_name:
            self.select_vpc_by_name(vpc_name)
        else:
            self.select_first_vpc()

        self.fill_form(name=nat_name, desc=desc)
        self.submit(text=B.CREATE_BUTTON_NAME)
        
        return nat_name