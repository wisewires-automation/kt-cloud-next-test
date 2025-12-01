""" Network Interface POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.actions import CreateButtonLocators as C
from pages.common import ToastLocators as T, ButtonLocators as B
from utils.name_generator import generate_name

class NICPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    NAME_INPUT = 'input[name="name"]'             # Network Interface 이름 입력 필드
    IP_INPUT = 'input[name="ipAddress"]'          # 사설 IP 입력 필드
    VPC_SELECT_NAME = "VPC를 선택해주세요."        # VPC 선택 셀렉트박스 placeholder
    SUBNET_SELECT_NAME = "Subnet을 선택해주세요."  # Subnet 선택 셀렉트박스 placeholder

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    # ============================================================
    # PROPERTIES
    # ============================================================ 
    @property
    def name_input(self):
        """NIC 생성 모달 - NIC 이름 입력 필드 locator"""
        return self.page.locator(self.NAME_INPUT)

    @property
    def ip_input(self):
        """NIC 생성 모달 - 사설 IP 입력 필드 locator"""
        return self.page.locator(self.IP_INPUT)

    @property
    def vpc_select(self):
        """NIC 생성 모달 - VPC 선택용 셀렉트박스 locator"""
        return self.page.get_by_role("combobox").filter(
            has_text=self.VPC_SELECT_NAME
        ).first

    @property
    def subnet_select(self):
        """NIC 생성 모달 - Subnet 선택용 combobox locator"""
        return self.page.get_by_role("combobox").filter(
            has_text=self.SUBNET_SELECT_NAME
        ).first

    @property
    def options(self):
        """공통 셀렉트 박스 옵션 locator"""
        return self.page.locator(".s-select-options-container .s-select-item--option")

    @property
    def security_row(self):
        """보안 그룹 리스트에서 'default' 보안 그룹이 위치한 row locator"""
        return self.page.get_by_role("row").filter(has_text="default").first

    @property
    def security_checkbox(self):
        """'default' 보안 그룹 row 내 체크박스 locator"""
        return self.security_row.locator('input[type="checkbox"]').first

    @property
    def confirm_button(self):
        """NIC 생성 모달 - 생성(확인) 버튼 locator"""
        return self.page.get_by_role("button", name=B.CREATE_BUTTON_NAME)
    
    # ============================================================
    # ACTIONS
    # ============================================================
    def fill_form(self, name: str, ip: str):
        """NIC 생성 폼에 이름 / 사설 IP 입력"""
        self.name_input.fill(name)
        self.ip_input.fill(ip)

    def select_vpc_option_by_index(self, idx: int = 0):
        """VPC 셀렉트 박스에서 인덱스로 VPC 선택"""
        self.vpc_select.click()
        self.options.nth(idx).click()

    def select_subnet_option_by_index(self, idx: int = 0):
        """Subnet 셀렉트 박스에서 인덱스로 Subnet 선택"""
        self.subnet_select.click()
        self.options.nth(idx).click()

    def click_security_checkbox(self, timeout: int = 10000):
        """'default' 보안 그룹 체크박스 클릭"""
        expect(self.security_checkbox).to_be_visible(timeout=timeout)
        self.security_checkbox.click()

    def submit_nic(self, timeout: int = 20000):
        """NIC 생성 버튼 클릭 및 생성 성공 토스트 검증"""
        # DOM에는 붙어 있는지 확인
        expect(self.confirm_button).to_be_attached(timeout=timeout)

        # viewport에서 보이지 않아 강제 클릭
        self.confirm_button.evaluate("el => el.click()")

        expect(self.page.get_by_text(T.CREATE_SUCCESS_TEXT)).to_be_visible(timeout=timeout)

    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_nic(self, select_network: bool = False) -> str:
        """Network Interface 생성 플로우"""
        nic_name = generate_name(prefix="QA-NIC-")
        self.open_create_modal(C.NIC_CREATE)

        self.fill_form(name=nic_name)

        if select_network:
            self.select_vpc_option_by_index()
            self.select_subnet_option_by_index()

        self.submit_nic()

        return nic_name