""" Volume POM """

from playwright.sync_api import Page, expect
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.locators.common import ToastLocators as T, ButtonLocators as B
from utils.namer import make_name

class VolumePage:

    NAME_INPUT = 'input[name="name"]'        # Volume 이름
    DESC_INPUT = 'input[name="description"]' # Volume 설명
    SIZE_INPUT = 'input[name="size"]'        # Volume 용량
    VOLUME_SELECT_NAME = "옵션을 선택하세요"    # Volume 유형, 가용 영역 선택 Placeholder
    CREATE_SUCCESS_TEXT = "Volume 생성 성공"

    def __init__(self, page: Page):
        self.page = page

        self.volume_nav_button = page.get_by_role("button", name=S.VOLUME_MENU, exact=True)
        self.volume_create_button = (page.locator("button").filter(has_text=C.VOLUME_CREATE).first)

        self.name_input = page.locator(self.NAME_INPUT)
        self.desc_input = page.locator(self.DESC_INPUT)
        self.size_input = page.locator(self.SIZE_INPUT)

        self.volumne_select = (self.page.get_by_role("combobox").filter(has_text=self.VOLUME_SELECT_NAME).first)
        self.volumne_options = self.page.locator(".s-select-options-container .s-select-item--option")

        self.confirm_button = page.get_by_role("button", name=B.CONFIRM_BUTTON, exact=True)

    def open_volume_create(self, timeout: int = 10000):
        expect(self.volume_nav_button).to_be_visible(timeout=timeout)
        self.volume_nav_button.click()

        expect(self.volume_create_button).to_be_visible(timeout=timeout)
        self.volume_create_button.click()
    
    def select_option_by_index(self, idx: int = 0):
        self.volumne_select.click()
        self.volumne_options.nth(idx).click()

    def submit(self, timeout: int = 10000):
        self.confirm_button.first.click()

        """Volume 생성 토스트 검증"""
        success_toast = self.page.get_by_text(self.CREATE_SUCCESS_TEXT)
        fail_toast = self.page.get_by_text(T.CREATE_FAIL_TEXT)
        
        try:
            expect(success_toast).to_be_visible(timeout=timeout)
        except Exception:
            try:
                expect(fail_toast).to_be_visible(timeout=timeout)
                raise AssertionError("Volumn 생성 실패")
            except Exception:
                raise

    def create_volume(
            self, 
            name_prefix: str = "QA-VOLUME-", 
            desc: str = "test volume 입니다",
            size: str = "128") -> str:
        
        volume_name = make_name(prefix=name_prefix)

        self.open_volume_create()
        self.name_input.fill(volume_name)
        self.desc_input.fill(desc)
        self.select_option_by_index() # Volume 유형
        self.size_input.fill(size)
        self.select_option_by_index() # 가용 영역 유형
        self.submit()

        return volume_name