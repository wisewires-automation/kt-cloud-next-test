""" NAT Gateway POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.common import ToastLocators as T, ButtonLocators as B
from utils.name_generator import generate_name
import time

class NATPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    NAME_INPUT = 'input[name="name"]'       # NAT Gateway 이름 입력 필드
    VPC_SELECT_NAME = "VPC를 선택하세요"      # VPC 선택 셀렉트박스 placeholder 텍스트
    ROUTE_SELECT_NAME = "연결 대상을 선택하세요"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    # ============================================================
    # PROPERTIES
    # ============================================================ 
    @property
    def name_input(self):
        """NAT Gateway 생성 모달 - 이름 입력 필드 locator"""
        return self.page.locator(self.NAME_INPUT)

    @property
    def vpc_select(self):
        """NAT Gateway 생성 모달 - VPC 선택용 셀렉트박스 locator"""
        return self.page.get_by_role("combobox").filter(
            has_text=self.VPC_SELECT_NAME
        ).first

    @property
    def rut_select(self):
        """NAT Gateway 생성 모달 - route tables 선택용 셀렉트박스 locator"""
        return self.page.get_by_role("combobox").filter(
            has_text=self.ROUTE_SELECT_NAME
        ).first
    
    @property
    def vpc_select_box(self):
        """NAT Gateway 생성 모달 - VPC 셀렉트 박스 선택 locator"""
        return self.page.locator("div.s-select-container").nth(1)

    @property
    def rut_select_box(self):
        """NAT Gateway 생성 모달 - route tables 셀렉트 박스 선택 locator"""
        return self.page.locator("div.s-select-container").nth(2)

    # ============================================================
    # ACTIONS
    # ============================================================
    def fill_form(self, name: str):
        """NAT Gateway 생성 모달에 이름 입력"""
        self.name_input.fill(name)

    def select_vpc_by_name(self, vpc_name: str, timeout: int = 10000):
        """VPC 이름으로 VPC 선택"""
        self.vpc_select_box.click()
        vpc_choice = self.vpc_select_box.locator("label", has_text=vpc_name)
        expect(vpc_choice).to_be_visible(timeout=timeout)
        vpc_choice.click()

    def select_first_vpc(self):
        """첫 번째 VPC 선택"""
        self.vpc_select_box.click()
        self.vpc_select_box.nth(0).click()

    def select_rut_by_name(self, rut_name:str, timeout:int=10000):
        """route tables 이름으로 route tables 선택"""
        self.rut_select_box.click()
        rut_label = self.rut_select_box.locator("label", has_text=rut_name)
        expect(rut_label).to_be_visible(timeout=timeout)
        rut_label.click()

    def select_first_rut(self):
        """첫 번째 route tables 선택"""
        self.rut_select_box.click()
        self.rut_select_box.nth(0).click()

    # ============================================================
    # 실행 함수
    # ============================================================

    #nat gateway 생성
    def create_nat(self, vpc_name: str = "", rut_name: str="") -> str:
        """NAT Gateway 생성 플로우"""
        nat_name = generate_name(prefix="QA-NAT-")
        self.page.locator(".s-button.s-button--medium.s-button--primary", has_text="NAT Gateway 생성").click()
        # 낫 게이트 웨이 이름 기입
        self.fill_form(name=nat_name)
        # VPC 명이 있을 경우 해당 이름으로 선택, 없을 경우 첫 번째 옵션 선택
        if vpc_name:
            self.select_vpc_by_name(vpc_name)
        else:
            self.select_first_vpc()
        time.sleep(5)
        #연결 대상 선택
        if rut_name:
            self.select_rut_by_name(rut_name)
        else:
            self.select_first_rut()
        #'확인' 버튼 클릭
        self.click_button(text=B.CONFIRM_TEXT)
        
        return nat_name

    #nat gateway 삭제
    def delete_nat(self, nat_gateway_name: str = "") -> str:
        """NAT Gateway 삭제 플로우"""
        #속도가 빨라 테이블 렌더 전에 이벤트문법 작동 방지용으로 sleep 걸었습니다 
        time.sleep(5)
        self.page.locator('a', has_text=nat_gateway_name).click()
        self.open_delete_modal()
        self.run_delete_flow()