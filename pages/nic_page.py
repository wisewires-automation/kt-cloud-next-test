""" Network Interface POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.locators.common import ToastLocators as T, ButtonLocators as B
from utils.namer import make_name

class NICPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    NAME_INPUT = 'input[name="name"]'           # Network Interface 이름
    IP_INPUT = 'input[name="ipAddress"]'        # 사설 IP
    VPC_SELECT_NAME = "VPC를 선택해주세요."         # VPC 선택 Placeholder
    SUBNET_SELECT_NAME = "Subnet을 선택해주세요."   # Subnet 선택 Placeholder

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self.vpc_select = (self.page.get_by_role("combobox").filter(has_text=self.VPC_SELECT_NAME).first)
        self.subnet_select = (self.page.get_by_role("combobox").filter(has_text=self.SUBNET_SELECT_NAME).first)
        self.options = self.page.locator(".s-select-options-container .s-select-item--option")

        self.security_row = page.get_by_role("row").filter(has_text="default").first
        self.security_checkbox = self.security_row.locator('input[type="checkbox"]').first

        self.confirm_button = page.get_by_role("button",name=B.CREATE_BUTTON_NAME)

    # ============================================================
    # PROPERTIES (locator 객체를 반환)
    # ============================================================ 
    @property
    def name_input(self):
        """모달 - NIC 이름 입력 필드"""
        return self.page.locator(self.NAME_INPUT)

    @property
    def ip_input(self):
        """모달 - IP 입력 필드"""
        return self.page.locator(self.IP_INPUT)
    
    # ============================================================
    # ACTIONS
    # ============================================================
    def fill_form(self, name: str, ip: str):
        """NIC 생성 폼 작성"""
        self.name_input.fill(name)
        self.ip_input.fill(ip)

    def select_vpc_option_by_index(self, idx: int = 0):
        self.vpc_select.click()
        self.options.nth(idx).click()

    def select_subnet_option_by_index(self, idx: int = 0):
        self.subnet_select.click()
        self.options.nth(idx).click()

    def click_security_checkbox(self, timeout: int = 10000):
        expect(self.security_checkbox).to_be_visible(timeout=timeout)
        self.security_checkbox.click()

    def submit_nic(self, timeout: int = 20000):
        # DOM에는 붙어 있는지 확인
        expect(self.confirm_button).to_be_attached(timeout=timeout)

        # viewport에서 보이지 않아 강제 클릭
        self.confirm_button.evaluate("el => el.click()")

        expect(self.page.get_by_text(T.CREATE_SUCCESS_TEXT)).to_be_visible(timeout=timeout)

    def create_nic(self, select_network: bool = False) -> str:
        nic_name = make_name(prefix="QA-NIC-")
        self.fill_form(name=nic_name)

        if select_network:
            self.select_vpc_option_by_index()
            self.select_subnet_option_by_index()

        self.submit_nic()

        return nic_name