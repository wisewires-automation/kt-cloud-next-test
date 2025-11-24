""" Security Group POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.locators.common import ToastLocators as T, ButtonLocators as B
from utils.namer import make_name

class SGPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    NAME_INPUT = 'input[name="name"]'        # Security Group 이름 입력 필드
    DESC_INPUT = 'input[name="description"]' # Security Group 설명 입력 필드

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    # ============================================================
    # PROPERTIES
    # ============================================================ 
    @property
    def name_input(self):
        """Security Group 생성 모달 - 이름 입력 필드 locator"""
        return self.page.locator(self.NAME_INPUT)

    @property
    def desc_input(self):
        """Security Group 생성 모달 - 설명 입력 필드 locator"""
        return self.page.locator(self.DESC_INPUT)
    
    # ============================================================
    # ACTIONS
    # ============================================================
    def fill_form(self, name: str):
        """Security Group 생성 모달에 이름/설명 입력"""
        self.name_input.fill(name)

    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_sg(self) -> str:
        """Security Group 생성 플로우"""
        sg_name = make_name(prefix="QA-SG-")
        self.fill_form(name=sg_name)
        self.submit(text=B.CREATE_BUTTON_NAME)
        return sg_name