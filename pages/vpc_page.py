""" VPC POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.actions import CreateButtonLocators as C

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
    def enter_name(self, name: str):
        """VPC 이름 입력"""
        self.name_input.fill(name)

    def enter_cidr(self, cidr: str):
        """VPC CIDR 입력"""
        self.cidr_input.fill(cidr)

    def fill_form(self, name: str, cidr: str):
        """VPC 모달 폼 입력"""
        self.enter_name(name)
        self.enter_cidr(cidr)

    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_vpc(self, vpc_name: str, cidr: str, timeout: int = 10000) -> str:
        """VPC 생성 플로우"""
        self.open_create_modal(C.VPC_CREATE)
        self.fill_form(name=vpc_name, cidr=cidr)
        self.click_button()
        expect(self.page.get_by_text(self.CREATE_SUCCESS_TEXT)).to_be_visible(timeout=timeout)

        return vpc_name
    
    def update_vpc(self, vpc_name: str, new_name: str):
        """VPC 수정 플로우"""
        self.go_link_by_name(name=vpc_name)
        self.run_rename_flow(new_name=new_name)
    
    def delete_vpc(self, vpc_name: str):
        """VPCL 삭제 플로우"""
        # self.go_link_by_name(name=vpc_name)
        self.open_delete_modal()
        self.run_delete_flow()