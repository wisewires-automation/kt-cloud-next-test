""" Server POM """

from playwright.sync_api import Page, expect
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.locators.common import ToastLocators as T, ButtonLocators as B
from utils.namer import make_name

from pages.vpc_page import VPCPage
from pages.subnet_page import SubnetPage
from pages.nic_page import NICPage
from pages.kp_page import KPPage

SERVER_IMAGE_TAB = ["OS 이미지", "서버 이미지", "서버 스냅샷"]
SERVER_SPEC_TAB = ["AMD (1세대)", "INTEL (1세대)", "DEV"]

class ServerPage:

    AZ_SELECT_NAME = "az 선택"            # Availability Zone 선택 placeholder
    AZ_DEFAULT_NAME = "DX-G-GB-A"
    SERVER_NAME_INPUT_PLACEHOLDER = "서버 이름을 입력하세요."  # Server 이름
    VPC_SELECT_NAME = "vpc 선택"            # VPC 선택 placeholder
    SUBNET_SELECT_NAME = "subnet 선택"      # Subnet 선택 placeholder
    KP_SELECT_NAME = "옵션을 선택하세요"      # Key Pair 선택 placeholder
    NIC_CREATE_BUTTON_TEXT = "신규 NIC 생성"
    CONFIRM_BUTTON_NAME = "서버 생성"

    def __init__(self, page: Page):
        self.page = page
        self.vpc_page = VPCPage(page)
        self.subnet_page = SubnetPage(page)
        self.nic_page = NICPage(page)
        self.kp_page = KPPage(page)

        self.server_nav_button = page.get_by_role("button", name=S.SERVER_MENU, exact=True)
        self.server_create_button = (page.locator("button").filter(has_text=C.SERVER_CREATE).first)

        self.radio_group = page.locator("div[role='radiogroup']")

        self.az_select = self.page.get_by_role("combobox").filter(has_text=self.AZ_SELECT_NAME)
        self.az_option = self.page.get_by_role("option", name=self.AZ_DEFAULT_NAME)
        self.server_name_input = page.get_by_placeholder(self.SERVER_NAME_INPUT_PLACEHOLDER)

        self.vpc_select = self.page.get_by_role("combobox").filter(has_text=self.VPC_SELECT_NAME)
        self.subnet_select = self.page.get_by_role("combobox").filter(has_text=self.SUBNET_SELECT_NAME)

        self.kp_select = self.page.get_by_role("combobox").filter(has_text=self.KP_SELECT_NAME)
        self.options = self.page.locator(".s-select-options-container .s-select-item--option")

        self.create_vpc_button = page.locator("button").filter(has_text=C.VPC_CREATE)
        self.create_subnet_button = page.locator("button").filter(has_text=C.SUBNET_CREATE)
        self.create_nic_button = page.locator("button").filter(has_text=self.NIC_CREATE_BUTTON_TEXT)
        self.create_kp_button = page.locator("button").filter(has_text=C.KP_CREATE)

        self.confirm_button = page.get_by_role("button", name=self.CONFIRM_BUTTON_NAME)

    # ===== 공통 동작 =====
    def go_server_page(self, timeout: int = 10000):
        expect(self.server_nav_button).to_be_visible(timeout=timeout)
        self.server_nav_button.click()

        expect(self.server_create_button).to_be_visible(timeout=timeout)
        self.server_create_button.click()
    
    # TODO: select_server_image_tab

    def select_server_image(self, index:int = 0, timeout: int = 10000):
        labels = self.radio_group.nth(1).locator("label[data-slot='label']")
        length = labels.count()
        print("server spec image length =", length)
        option_label = (self.radio_group.nth(0).locator("label[data-slot='label']").nth(index))

        expect(option_label).to_be_visible(timeout=timeout)
        option_label.click()

    # TODO: select_server_spec_tab

    def select_server_spec(self, index:int = 0, timeout: int = 10000):
        labels = self.radio_group.nth(1).locator("label[data-slot='label']")
        length = labels.count()
        print("server spec option length =", length)
        option_label = (self.radio_group.nth(1).locator("label[data-slot='label']").nth(index))

        expect(option_label).to_be_visible(timeout=timeout)
        option_label.click()

    def fill_basic_info(self) -> str:
        self.az_select.click()
        # NOTE: 첫번째 옵션 값만 클릭됨 (원하는 index로 선택 할 수 있게 변경 필요)
        self.az_option.first.click()

        server_name = make_name(prefix="QA-SERVER-")
        self.server_name_input.fill(server_name)

        return server_name
    
    # VPC
    def create_vpc(self) -> str:
        self.create_vpc_button.click()
        vpc_name = self.vpc_page.create_vpc()
        return vpc_name

    def select_vpc_by_name(self, vpc_name: str, timeout: int = 10000):
        self.vpc_select.click()

        option = self.page.get_by_role("option", name=vpc_name)
        expect(option).to_be_visible(timeout=timeout)
        option.click()

    # Subnet
    def create_subnet(self) -> str:
        self.create_subnet_button.click()
        subnet_name = self.subnet_page.create_subnet()
        return subnet_name

    def select_subnet_by_name(self, subnet_name: str, timeout: int = 10000):
        self.subnet_select.click()

        option = self.page.get_by_role("option", name=subnet_name)
        expect(option).to_be_visible(timeout=timeout)
        option.click()

    # NIC
    def create_nic(self) -> str:
        self.create_nic_button.click()
        nic_name = self.nic_page.create_nic()
        return nic_name

    def select_nic_by_name(self, nic_name: str, timeout: int = 10000):
        nic_row = self.page.locator('label[data-slot="label"]').filter(has_text=nic_name).first

        expect(nic_row).to_be_visible(timeout=timeout)
        nic_row.click() 
    
    # Key Pair
    def creat_kp(self) -> str:
        self.create_kp_button.click()
        kp_name = self.kp_page.create_kp()
        return kp_name

    def select_key_by_name(self, key_name: str, timeout: int = 10000):
        self.kp_select.click()
        option = self.page.locator(".s-select-item--option").filter(has_text=key_name).first
        expect(option).to_be_visible(timeout=timeout)
        option.click()

    def submit(self, timeout: int = 20000):
        expect(self.confirm_button).to_be_visible(timeout=timeout)
        self.confirm_button.click()

        success_toast = self.page.get_by_text(T.CREATE_SUCCESS_TEXT)
        fail_toast = self.page.get_by_text(T.CREATE_FAIL_TEXT)
        
        try:
            expect(success_toast).to_be_visible(timeout=timeout)
        except Exception:
            try:
                expect(fail_toast).to_be_visible(timeout=timeout)
                raise AssertionError("서버 생성 실패")
            except Exception:
                raise

