""" Volume POM """

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.locators.common import ToastLocators as T, ButtonLocators as B
from utils.namer import make_name

class VolumePage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    NAME_INPUT = 'input[name="name"]'        # Volume 이름
    DESC_INPUT = 'input[name="description"]' # Volume 설명
    SIZE_INPUT = 'input[name="size"]'        # Volume 용량
    VOLUME_SELECT_NAME = "옵션을 선택하세요"    # Volume 유형, 가용 영역 선택 Placeholder
    CREATE_SUCCESS_TEXT = "Volume 생성 성공"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self.volumne_select = (self.page.get_by_role("combobox").filter(has_text=self.VOLUME_SELECT_NAME).first)
        self.volumne_options = self.page.locator(".s-select-options-container .s-select-item--option")

    # ============================================================
    # PROPERTIES (locator 객체를 반환)
    # ============================================================
    @property
    def name_input(self):
        """모달 - VPC 이름 입력 필드"""
        return self.page.locator(self.NAME_INPUT)

    @property
    def desc_input(self):
        """모달 - 설명 입력 필드"""
        return self.page.locator(self.DESC_INPUT)
    
    @property
    def size_input(self):
        """모달 - 사이즈 입력 필드"""
        return self.page.locator(self.SIZE_INPUT)
    
    # ============================================================
    # ACTIONS
    # ============================================================
    def fill_form(self, name: str, desc: str, size: str):
        """VPC 이름, CIDR 입력"""
        self.name_input.fill(name)
        self.desc_input.fill(desc)

    def select_option_by_index(self, idx: int = 0):
        self.volumne_select.click()
        self.volumne_options.nth(idx).click()

    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_volume(self, desc: str = "test volume 입니다", size: str = "128") -> str:
        volume_name = make_name(prefix="QA-VOLUME-")

        self.fill_form(name=volume_name, desc=desc)
        self.select_option_by_index() # Volume 유형

        self.size_input.fill(size)
        self.select_option_by_index() # 가용 영역 유형
        
        self.submit()

        return volume_name