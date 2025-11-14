from playwright.sync_api import Page, expect
from utils.namer import make_name

SERVER_IMAGE_TAB = ["OS 이미지", "서버 이미지", "서버 스냅샷"]

class ServerPage:

    # ===== selector / text 상수 =====
    SERVER_NAV_BUTTON_NAME = "Server"
    SERVER_CREATE_BUTTON_NAME = "Server 생성"

    AZ_SELECT_NAME = "az 선택"            # Availability Zone 선택 placeholder
    AZ_DEFAULT_NAME = "DX-G-GB-A"
    SERVER_NAME_INPUT_PLACEHOLDER = '서버 이름을 입력하세요.'  # Server 이름

    VPC_SELECT_NAME = "vpc 선택"         # VPC 선택 placeholder
    VPC_DEFAULT_VALUE = "TEST_VPCS29Q"
    SUBNET_SELECT_NAME = "subnet 선택"   # Subnet 선택 placeholder
    SUBNET_DEFAULT_VALUE = "sub-name-01"
    KP_SELECT_NAME = "옵션을 선택하세요"       # Key Pair 선택 placeholder

    VOLUME_CREATE_BUTTON_TEXT = "Volume 생성"
    SUBNET_CREATE_BUTTON_TEXT = "Subnet 생성"
    NIC_CREATE_BUTTON_TEXT = "신규 NIC 생성"

    CONFIRM_BUTTON_NAME = "서버 생성"

    SERVER_CREATE_SUCCESS_TEXT = "생성 완료"
    SERVER_CREATE_FAIL_TEXT = "생성 실패"

    def __init__(self, page: Page):
        self.page = page

        self.server_nav_button = page.get_by_role("button", name=self.SERVER_NAV_BUTTON_NAME, exact=True)
        self.server_create_button = (page.locator("button").filter(has_text=self.SERVER_CREATE_BUTTON_NAME).first)

        self.image_group = page.locator("div[role='radiogroup']")

        self.az_select = self.page.get_by_role("combobox").filter(has_text=self.AZ_SELECT_NAME)
        self.az_option = self.page.get_by_role("option", name=self.AZ_DEFAULT_NAME)
        self.server_name_input = page.get_by_placeholder(self.SERVER_NAME_INPUT_PLACEHOLDER)

        self.vpc_select = self.page.get_by_role("combobox").filter(has_text=self.VPC_SELECT_NAME)
        self.vpc_option = self.page.get_by_role("option", name=self.VPC_DEFAULT_VALUE)
        self.subnet_select = self.page.get_by_role("combobox").filter(has_text=self.SUBNET_SELECT_NAME)
        self.subnet_option = self.page.get_by_role("option", name=self.SUBNET_DEFAULT_VALUE)

        self.kp_select = self.page.get_by_role("combobox").filter(has_text=self.KP_SELECT_NAME)
        self.options = self.page.locator(".s-select-options-container .s-select-item--option")

        self.create_nic_button = page.locator("button").filter(has_text=self.NIC_CREATE_BUTTON_TEXT)

        self.confirm_button = page.get_by_role("button", name=self.CONFIRM_BUTTON_NAME)

    # ===== 공통 동작 =====
    def go_server_page(self, timeout: int = 10000):
        expect(self.server_nav_button).to_be_visible(timeout=timeout)
        self.server_nav_button.click()

        expect(self.server_create_button).to_be_visible(timeout=timeout)
        self.server_create_button.click()

    def select_server_image(self, index:int = 0, timeout: int = 10000):
        option_label = (self.image_group.nth(0).locator("label[data-slot='label']").nth(index))

        expect(option_label).to_be_visible(timeout=timeout)
        option_label.click()

    def select_server_spec(self, index:int = 0, timeout: int = 10000):
        option_label = (self.image_group.nth(1).locator("label[data-slot='label']").nth(1))

        expect(option_label).to_be_visible(timeout=timeout)
        option_label.click()

    def fill_basic_info(self) -> str:
        self.az_select.click()
        self.az_option.first.click()

        server_name = make_name(prefix="SERVER-", suffix_len=4)
        self.server_name_input.fill(server_name)

        return server_name

    def select_vpc_option_by_index(self, idx: int = 0):
        self.vpc_select.click()
        self.vpc_option.first.click()

    def select_subnet_option_by_index(self, idx: int = 0):
        self.subnet_select.click()
        self.subnet_option.first.click()

    def select_nic(self, timeout: int = 10000):
        option_label = (self.image_group.nth(2).locator("label[data-slot='label']").nth(1))

        expect(option_label).to_be_visible(timeout=timeout)
        option_label.click()

    def select_kp_option(self, index: int = 0):
        self.kp_select.click()
        self.options.nth(index).click()

    def submit(self, timeout: int = 20000):
        expect(self.confirm_button).to_be_visible(timeout=timeout)
        self.confirm_button.click()

        """서버 생성 토스트 검증"""
        success_toast = self.page.get_by_text(self.SERVER_CREATE_SUCCESS_TEXT)
        fail_toast = self.page.get_by_text(self.SERVER_CREATE_FAIL_TEXT)
        
        try:
            expect(success_toast).to_be_visible(timeout=timeout)
        except Exception:
            try:
                expect(fail_toast).to_be_visible(timeout=timeout)
                raise AssertionError("서버 생성 실패")
            except Exception:
                raise

