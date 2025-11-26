""" Internet Gateway POM """

from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.locators.common import ButtonLocators as B
from pages.locators.actions import CreateButtonLocators as C
from utils.name_generator import generate_name

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
    def enter_name(self, name: str):
        """Internet Gateway 이름 입력"""
        self.name_input.fill(name)
    
    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_ig(self) -> str:
        """Internet Gateway 생성 플로우"""
        ig_name = generate_name(prefix="QA-IG-")

        self.open_create_modal(C.IG_CREATE)
        self.enter_name(name=ig_name)
        self.click_button(text=B.CREATE_BUTTON_NAME)

        return ig_name
    
    def delete_ig(self, ig_name: str):
        """Internet Gateway 삭제 플로우"""
        self.go_link_by_name(name=ig_name)
        self.open_delete_modal()
        self.run_delete_flow()