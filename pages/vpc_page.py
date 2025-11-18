""" VPC POM """

from playwright.sync_api import Page, expect
from utils.namer import make_name

class VPCPage:

    # ===== selector / text 상수 =====
    VPC_NAV_BUTTON_NAME = "VPC"
    VPC_CREATE_BUTTON_NAME = "VPC 생성"

    VPC_NAME_INPUT = 'input[name="name"]'           # VPC 이름
    VPC_CIDR_INPUT = 'input[name="cidr"]'           # CIDR 주소

    CONFIRM_BUTTON_NAME = "확인"
    CREATE_SUCCESS_TEXT = "VPC 생성 성공"

    def __init__(self, page: Page):
        self.page = page

        self.vpc_nav_button = page.get_by_role("button", name=self.VPC_NAV_BUTTON_NAME, exact=True)
        self.vpc_create_button = (page.locator("button").filter(has_text=self.VPC_CREATE_BUTTON_NAME).first)

        self.name_input = page.locator(self.VPC_NAME_INPUT)
        self.cidr_input = page.locator(self.VPC_CIDR_INPUT)

        self.confirm_button = page.get_by_role("button",name=self.CONFIRM_BUTTON_NAME)

    # ===== 공통 동작 =====
    def open_vpc_create(self, timeout: int = 10000):
        """VPC 메뉴 이동 후 'VPC 생성' 모달 오픈"""
        expect(self.vpc_nav_button).to_be_visible(timeout=timeout)
        self.vpc_nav_button.click()

        expect(self.vpc_create_button).to_be_visible(timeout=timeout)
        self.vpc_create_button.click()

    def fill_form(self, name: str, cidr: str, timeout: int = 10000):
        expect(self.name_input).to_be_visible(timeout=timeout)
        self.name_input.fill(name)

        expect(self.cidr_input).to_be_visible(timeout=timeout)
        self.cidr_input.fill(cidr)

    def submit(self, timeout: int = 20000):
        expect(self.confirm_button).to_be_enabled(timeout=timeout)
        self.confirm_button.click()

        """VPC 생성 성공 토스트 검증"""
        expect(self.page.get_by_text(self.CREATE_SUCCESS_TEXT)).to_be_visible(timeout=timeout)

    def create_vpc(self, name_prefix: str = "TEST_VPC", cidr: str = "10.0.0.0/8") -> str:
        vpc_name = make_name(prefix=name_prefix)
        
        self.fill_form(name=vpc_name, cidr=cidr)
        self.submit()

        return vpc_name