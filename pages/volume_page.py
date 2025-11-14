from playwright.sync_api import Page, expect
from utils.namer import make_name

class VolumePage:

    # ===== selector / text 상수 =====
    VOLUME_NAV_BUTTON_NAME = "Volume"
    VOLUME_CREATE_BUTTON_NAME = "Volume 생성"

    VOLUME_NAME_INPUT = 'input[name="name"]'        # Volume 이름
    VOLUME_DESC_INPUT = 'input[name="description"]' # Volume 설명
    VOLUME_SIZE_INPUT = 'input[name="size"]'        # Volume 용량

    VOLUME_SELECT_NAME = "옵션을 선택하세요"           # Volume 유형, 가용 영역 선택 Placeholder

    CONFIRM_BUTTON_NAME = "확인"

    VOLUME_CREATE_SUCCESS_TEXT = "Volume 생성 성공"
    VOLUME_CREATE_FAIL_TEXT = "생성 실패"

    def __init__(self, page: Page):
        self.page = page

        self.volume_nav_button = page.get_by_role("button", name=self.VOLUME_NAV_BUTTON_NAME, exact=True)
        self.volume_create_button = (page.locator("button").filter(has_text=self.VOLUME_CREATE_BUTTON_NAME).first)

        self.name_input = page.locator(self.VOLUME_NAME_INPUT)
        self.desc_input = page.locator(self.VOLUME_DESC_INPUT)
        self.size_input = page.locator(self.VOLUME_SIZE_INPUT)

        self.volumne_select = (self.page.get_by_role("combobox").filter(has_text=self.VOLUME_SELECT_NAME).first)
        self.volumne_options = self.page.locator(".s-select-options-container .s-select-item--option")

        self.confirm_button = page.get_by_role("button", name=self.CONFIRM_BUTTON_NAME, exact=True)

    # ===== 공통 동작 =====
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
        success_toast = self.page.get_by_text(self.VOLUME_CREATE_SUCCESS_TEXT)
        fail_toast = self.page.get_by_text(self.VOLUME_CREATE_FAIL_TEXT)
        
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
            name_prefix: str = "VOLUME-", 
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