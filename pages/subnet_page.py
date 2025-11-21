""" Subnet POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.locators.common import ToastLocators as T, ButtonLocators as B
from utils.namer import make_name

class SubnetPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    VPC_SELECT_NAME = "VPC를 선택해주세요"         # VPC 선택 Placeholder
    NAME_INPUT = 'input[name="name"]'    # Subnet 이름
    CIDR_INPUT = 'input[name="cidr"]'    # Subnet CIDR 블록
    CREATE_SUCCESS_TEXT = "Subnet 생성 성공"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    # ============================================================
    # PROPERTIES (locator 객체를 반환)
    # ============================================================ 
    @property
    def name_input(self):
        """모달 - VPC 이름 입력 필드"""
        return self.page.locator(self.NAME_INPUT)

    @property
    def cidr_input(self):
        """모달 - CIDR 주소 입력 필드"""
        return self.page.locator(self.CIDR_INPUT)

    @property
    def vpc_select(self):
        """VPC 셀렉트 박스"""
        return (self.page.get_by_role("combobox").filter(has_text=self.VPC_SELECT_NAME).first)    
    
    @property
    def vpc_label(self):
        """VPC 셀렉트 박스"""
        return self.page.locator("label.s-select-radio-label")
    
    @property
    def vpc_option(self):
        """VPC 셀렉트 박스"""
        return self.page.locator(".s-select-options-container .s-select-item--option")

    # ============================================================
    # ACTIONS
    # ============================================================
    def select_first_vpc(self):
        """첫번째 VPC 선택"""
        self.vpc_select.click()
        self.vpc_option.nth(0).click()

    def select_vpc_by_name(self, vpc_name: str, timeout: int = 10000):
        """VPC 명으로 VPC 선택"""
        self.vpc_select.click()

        vpc_label = self.vpc_label.filter(has_text=vpc_name).first
        expect(vpc_label).to_be_visible(timeout=timeout)
        vpc_label.click()

    def fill_form(self, name: str, cidr: str):
        """Subnet 이름, CIDR 입력"""
        self.name_input.fill(name)
        self.cidr_input.fill(cidr)

    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_subnet(self, cidr: str = "10.0.0.0/8", vpc_name: str = "QA-VPC-003", timeout: int = 10000) -> str:
        subnet_name = make_name(prefix="QA-SUB-")

        # VPC명이 없으면 첫번째 옵션 선택
        if vpc_name:
            self.select_vpc_by_name(vpc_name)
        else:
            self.select_first_vpc()

        self.fill_form(name=subnet_name, cidr=cidr)
        self.submit()
        expect(self.page.get_by_text(self.CREATE_SUCCESS_TEXT)).to_be_visible(timeout=timeout)

        return subnet_name