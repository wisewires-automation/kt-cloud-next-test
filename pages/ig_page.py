""" Internet Gateway POM """

from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.locators.common import ButtonLocators as B
from utils.namer import make_name

class IGPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    NAME_INPUT = 'input[name="name"]' # Internet Gateway 이름 입력 필드

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    # ============================================================
    # PROPERTIES
    # ============================================================
    @property
    def name_input(self):
        """Internet Gateway 생성 모달 - 이름 입력 필드 locator"""
        return self.page.locator(self.NAME_INPUT)
    
    # ============================================================
    # ACTIONS
    # ============================================================
    def fill_form(self, name: str):
        """ Internet Gateway 생성 모달에 이름 값 입력"""
        self.name_input.fill(name)
    
    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_ig(self) -> str:
        """Internet Gateway 생성 플로우"""
        ig_name = make_name(prefix="QA-IG-")
        self.fill_form(name=ig_name)
        self.click_button(text=B.CREATE_BUTTON_NAME)
        return ig_name