""" Internet Gateway POM """

from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.locators.common import ButtonLocators as B
from utils.namer import make_name

class IGPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    NAME_INPUT = 'input[name="name"]' # Internet Gateway 이름

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    # ============================================================
    # PROPERTIES (locator 객체를 반환)
    # ============================================================
    @property
    def name_input(self):
        """모달 - VPC 이름 입력 필드"""
        return self.page.locator(self.NAME_INPUT)
    
    # ============================================================
    # ACTIONS
    # ============================================================
    def fill_form(self, name: str):
        self.name_input.fill(name)
    
    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_ig(self) -> str:
        ig_name = make_name(prefix="QA-IG-")
        self.fill_form(name=ig_name)
        self.submit(text=B.CREATE_BUTTON_NAME)
        return ig_name