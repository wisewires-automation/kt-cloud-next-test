""" VPC POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.namer import make_name

class VPCPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    NAME_INPUT = 'input[name="name"]'    # VPC 이름 입력 필드
    CIDR_INPUT = 'input[name="cidr"]'    # CIDR 블록 입력 필드
    CREATE_SUCCESS_TEXT = "VPC 생성 성공"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    # ============================================================
    # PROPERTIES
    # ============================================================ 
    @property
    def name_input(self):
        """VPC 생성 모달 - VPC 이름 입력 필드 locator"""
        return self.page.locator(self.NAME_INPUT)

    @property
    def cidr_input(self):
        """VPC 생성 모달 - CIDR 블록 입력 필드 locator"""
        return self.page.locator(self.CIDR_INPUT)
    
    # ============================================================
    # ACTIONS
    # ============================================================
    def fill_form(self, name: str, cidr: str):
        """VPC 생성 모달에 VPC 이름/CIDR 입력"""
        self.name_input.fill(name)
        self.cidr_input.fill(cidr)

    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_vpc(self, cidr: str = "10.0.0.0/8", timeout: int = 10000) -> str:
        """ VPC 생성 플로우"""
        vpc_name = make_name(prefix="QA-VPC-")
        self.fill_form(name=vpc_name, cidr=cidr)
        self.submit()
        expect(self.page.get_by_text(self.CREATE_SUCCESS_TEXT)).to_be_visible(timeout=timeout)

        return vpc_name