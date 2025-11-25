""" VPC Peering POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.name_generator import generate_name

class VPCPeeringPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    NAME_INPUT = 'input[name="name"]'    # VPC Peering 이름 입력 필드

    VPC_SELECT_NAME = "VPC를 선택해주세요."
    PEERING_VPC_SELECT_NAME = "Peering 할 VPC를 선택해주세요."

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    # ============================================================
    # PROPERTIES
    # ============================================================ 
    @property
    def name_input(self):
        """생성 모달 - VPC Peering 이름 입력 필드 locator"""
        return self.page.locator(self.NAME_INPUT)

    @property
    def vpc_select(self):
        """생성 모달 - VPC 선택용 셀렉트박스 locator"""
        return self.page.get_by_role("combobox").filter(has_text=self.VPC_SELECT_NAME).first
    
    @property
    def p_vpc_select(self):
        """생성 모달 - Peering할 VPC 선택용 셀렉트박스 locator"""
        return (self.page.get_by_role("combobox").filter(has_text=self.PEERING_VPC_SELECT_NAME).first)
    
    @property
    def vpc_option_rows(self):
        return self.page.locator("div.s-select-item--option")

    @property
    def vpc_option_labels(self):
        return self.page.locator("label.s-select-radio-label")
    
    # ============================================================
    # ACTIONS
    # ============================================================
    def enter_name(self, name: str):
        """생성 모달에 VPC Perring 이름 입력"""
        self.name_input.fill(name)

    def _select_from_dropdown(self, trigger, item_text: str, timeout: int = 10000) -> None:
        """공통: 셀렉트박스 열고, 텍스트 포함된 옵션 선택"""
        expect(trigger).to_be_visible(timeout=timeout)
        trigger.click()

        # 옵션이 최소 1개는 뜰 때까지 대기
        expect(self.vpc_option_rows.first).to_be_visible(timeout=timeout)

        option_label = self.vpc_option_labels.filter(has_text=item_text).first
        expect(option_label).to_be_visible(timeout=timeout)

        option_label.click()

    def select_vpc_by_name(self, vpc_name: str, timeout: int = 10000) -> None:
        """첫 번째 VPC 선택"""
        self._select_from_dropdown(self.vpc_select, vpc_name, timeout)

    def select_peering_vpc_by_name(self, vpc_name: str, timeout: int = 10000) -> None:
        """Peering 대상 VPC 선택"""
        self._select_from_dropdown(self.p_vpc_select, vpc_name, timeout)

    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_vpc_peering(self, vpc_01: str, vpc_02: str) -> str:
        """VPC Peering 생성 플로우"""
        vpc_p_name = generate_name(prefix="QA-VPC-P-")

        # 이름 입력
        self.enter_name(name=vpc_p_name)

        # 첫 번째 VPC 선택
        self.select_vpc_by_name(vpc_name=vpc_01)

        # 두 번째 VPC 선택
        self.select_peering_vpc_by_name(vpc_name=vpc_02)

        # 확인 버튼
        self.click_button()

        return vpc_p_name