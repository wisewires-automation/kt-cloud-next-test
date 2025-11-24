""" Server POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.locators.common import ToastLocators as T, ButtonLocators as B
from utils.namer import make_name

from pages.vpc_page import VPCPage
from pages.subnet_page import SubnetPage
from pages.nic_page import NICPage
from pages.keypair_page import KeypairPage

SERVER_IMAGE_TAB = ["OS 이미지", "서버 이미지", "서버 스냅샷"]
SERVER_SPEC_TAB = ["AMD (1세대)", "INTEL (1세대)", "DEV"]


class ServerPage(BasePage):# ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    AZ_SELECT_NAME = "az 선택"                               # Availability Zone 선택 셀렉트박스 placeholder
    AZ_DEFAULT_NAME = "DX-G-GB-A"                            # 기본 AZ 옵션 이름
    SERVER_NAME_INPUT_PLACEHOLDER = "서버 이름을 입력하세요."   # 서버 이름 입력 필드 placeholder

    VPC_SELECT_NAME = "vpc 선택"                              # VPC 선택 셀렉트박스 placeholder
    SUBNET_SELECT_NAME = "subnet 선택"                        # Subnet 선택 셀렉트박스 placeholder
    KP_SELECT_NAME = "옵션을 선택하세요"                        # Key Pair 선택 셀렉트박스 placeholder

    NIC_CREATE_BUTTON_TEXT = "신규 NIC 생성"                    # NIC 생성 버튼 텍스트
    CONFIRM_BUTTON_NAME = "서버 생성"                           # 서버 생성 버튼 텍스트

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self.vpc_page = VPCPage(page)
        self.subnet_page = SubnetPage(page)
        self.nic_page = NICPage(page)
        self.kp_page = KeypairPage(page)

    # ============================================================
    # PROPERTIES
    # ============================================================
    @property
    def server_nav_button(self):
        """왼쪽 사이드바 - 서버 메뉴 버튼 locator"""
        return self.page.get_by_role("button", name=S.SERVER_MENU, exact=True)

    @property
    def server_create_button(self):
        """서버 목록 페이지 - '서버 생성' 버튼 locator"""
        return self.page.locator("button").filter(has_text=C.SERVER_CREATE).first

    @property
    def radio_group(self):
        """서버 이미지 / 스펙 선택용 라디오 그룹 locator"""
        return self.page.locator("div[role='radiogroup']")

    @property
    def az_select(self):
        """AZ 선택 셀렉트박스 locator"""
        return self.page.get_by_role("combobox").filter(has_text=self.AZ_SELECT_NAME).first

    @property
    def az_option_default(self):
        """기본 AZ 옵션 locator"""
        return self.page.get_by_role("option", name=self.AZ_DEFAULT_NAME)

    @property
    def server_name_input(self):
        """서버 이름 입력 필드 locator"""
        return self.page.get_by_placeholder(self.SERVER_NAME_INPUT_PLACEHOLDER)

    @property
    def vpc_select(self):
        """VPC 선택 셀렉트박스 locator"""
        return self.page.get_by_role("combobox").filter(has_text=self.VPC_SELECT_NAME).first

    @property
    def subnet_select(self):
        """Subnet 선택 셀렉트박스 locator"""
        return self.page.get_by_role("combobox").filter(has_text=self.SUBNET_SELECT_NAME).first

    @property
    def kp_select(self):
        """Key Pair 선택 셀렉트박스 locator"""
        return self.page.get_by_role("combobox").filter(has_text=self.KP_SELECT_NAME).first

    @property
    def select_options(self):
        """공통 셀렉트 박스 옵션 locator"""
        return self.page.locator(".s-select-options-container .s-select-item--option")

    @property
    def create_vpc_button(self):
        """VPC '신규 생성' 버튼 locator"""
        return self.page.locator("button").filter(has_text=C.VPC_CREATE).first

    @property
    def create_subnet_button(self):
        """Subnet '신규 생성' 버튼 locator"""
        return self.page.locator("button").filter(has_text=C.SUBNET_CREATE).first

    @property
    def create_nic_button(self):
        """NIC '신규 NIC 생성' 버튼 locator"""
        return self.page.locator("button").filter(has_text=self.NIC_CREATE_BUTTON_TEXT).first

    @property
    def create_kp_button(self):
        """Key Pair '신규 생성' 버튼 locator"""
        return self.page.locator("button").filter(has_text=C.KP_CREATE).first

    @property
    def confirm_button(self):
        """'서버 생성' 버튼 locator"""
        return self.page.get_by_role("button", name=self.CONFIRM_BUTTON_NAME)

    # ============================================================
    # ACTIONS
    # ============================================================
    def go_server_page(self, timeout: int = 10000):
        """서버 생성 페이지로 이동"""
        expect(self.server_nav_button).to_be_visible(timeout=timeout)
        self.server_nav_button.click()

        expect(self.server_create_button).to_be_visible(timeout=timeout)
        self.server_create_button.click()

    # 서버 이미지 / 스펙 선택
    def select_server_image(self, index: int = 0, timeout: int = 10000):
        """서버 이미지 선택"""
        labels = self.radio_group.nth(0).locator("label[data-slot='label']")
        length = labels.count()
        print("server image option length =", length)

        option_label = labels.nth(index)
        expect(option_label).to_be_visible(timeout=timeout)
        option_label.click()

    def select_server_spec(self, index: int = 0, timeout: int = 10000):
        """서버 스펙 선택"""
        labels = self.radio_group.nth(1).locator("label[data-slot='label']")
        length = labels.count()
        print("server spec option length =", length)

        option_label = labels.nth(index)
        expect(option_label).to_be_visible(timeout=timeout)
        option_label.click()

    # 기본 정보 입력
    def fill_basic_info(self) -> str:
        """서버 기본 정보(AZ, 서버 이름) 입력"""
        self.az_select.click()
        # NOTE: 현재는 기본 AZ 옵션만 선택 (필요 시 index 기반 선택으로 확장 가능)
        self.az_option_default.first.click()

        server_name = make_name(prefix="QA-SERVER-")
        self.server_name_input.fill(server_name)

        return server_name

    # VPC 관련
    def create_vpc(self) -> str:
        """'신규 VPC 생성' 버튼 클릭 후 VPC 생성 플로우 호출"""
        self.create_vpc_button.click()
        vpc_name = self.vpc_page.create_vpc()
        return vpc_name

    def select_vpc_by_name(self, vpc_name: str, timeout: int = 10000):
        """VPC 이름으로 VPC 선택"""
        self.vpc_select.click()

        option = self.page.get_by_role("option", name=vpc_name)
        expect(option).to_be_visible(timeout=timeout)
        option.click()

    # Subnet 관련
    def create_subnet(self) -> str:
        """'신규 Subnet 생성' 버튼 클릭 후 Subnet 생성 플로우 호출"""
        self.create_subnet_button.click()
        subnet_name = self.subnet_page.create_subnet()
        return subnet_name

    def select_subnet_by_name(self, subnet_name: str, timeout: int = 10000):
        """Subnet 이름으로 Subnet 선택"""
        self.subnet_select.click()

        option = self.page.get_by_role("option", name=subnet_name)
        expect(option).to_be_visible(timeout=timeout)
        option.click()

    # NIC 관련
    def create_nic(self) -> str:
        """'신규 NIC 생성' 버튼 클릭 후 NIC 생성 플로우 호출"""
        self.create_nic_button.click()
        nic_name = self.nic_page.create_nic()
        return nic_name

    def select_nic_by_name(self, nic_name: str, timeout: int = 10000):
        """NIC 이름으로 NIC 선택"""
        nic_row = self.page.locator('label[data-slot="label"]').filter(has_text=nic_name).first

        expect(nic_row).to_be_visible(timeout=timeout)
        nic_row.click()

    # Key Pair 관련
    def creat_kp(self) -> str:
        """'신규 Key Pair 생성' 버튼 클릭 후 Key Pair 생성 플로우 호출"""
        self.create_kp_button.click()
        kp_name = self.kp_page.create_kp()
        return kp_name

    def select_key_by_name(self, key_name: str, timeout: int = 10000):
        """Key Pair 이름으로 Key Pair 선택"""
        self.kp_select.click()
        option = self.page.locator(".s-select-item--option").filter(has_text=key_name).first
        expect(option).to_be_visible(timeout=timeout)
        option.click()

    def submit(self, timeout: int = 20000):
        """서버 생성 버튼 클릭 및 생성 결과 토스트 검증"""
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
