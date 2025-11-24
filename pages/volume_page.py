""" Volume POM """

from playwright.sync_api import Page, expect, Locator
from pages.base_page import BasePage
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.locators.common import ToastLocators as T, ButtonLocators as B
from utils.namer import make_name

class VolumePage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    NAME_INPUT = 'input[name="name"]'        # Volume 이름 입력 필드
    DESC_INPUT = 'input[name="description"]' # Volume 설명 입력 필드
    SIZE_INPUT = 'input[name="size"]'        # Volume 용량 입력 필드
    VOLUME_SELECT_NAME = "옵션을 선택하세요"    # Volume 유형, 가용 영역 선택 Placeholder 입력 필드
    CREATE_SUCCESS_TEXT = "Volume 생성 성공"   # 생성 성공 토스트 메시지 텍스트

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    # ============================================================
    # PROPERTIES
    # ============================================================
    @property
    def name_input(self):
        """Volume 생성 모달 - Volume 이름 입력 필드 locator"""
        return self.page.locator(self.NAME_INPUT)

    @property
    def desc_input(self):
        """Volume 생성 모달 - 설명 입력 필드 locator"""
        return self.page.locator(self.DESC_INPUT)
    
    @property
    def size_input(self):
        """Volume 생성 모달 - 용량 입력 필드 locator"""
        return self.page.locator(self.SIZE_INPUT)
    
    @property
    def volume_select(self):
        """Volume 생성 모달 - 공통 선택 박스 locator"""
        return (self.page.get_by_role("combobox").filter(has_text=self.VOLUME_SELECT_NAME).first)
    
    @property
    def volume_options(self):
        """Volume 생성 모달 - 선택박스 옵션 목록 locator"""
        return self.page.locator(".s-select-options-container .s-select-item--option")
    # ============================================================
    # ACTIONS
    # ============================================================
    def fill_form(self, name: str, desc: str):
        """Volume 생성 모달에 이름/설명 입력"""
        self.name_input.fill(name)
        self.desc_input.fill(desc)

    def select_option_by_index(self, index: int = 0):
        """선택 박스에서 주어진 인덱스의 옵션 선택"""
        self.volume_select.click()
        self.volume_options.nth(index).click()
    
    def open_row_menu(self, volume_name: str, timeout: int = 10000):
        """Volume 리스트에서 특정 이름의 row에 있는 '…'(dropdown) 메뉴 버튼 클릭"""
        row = self._get_center_row_by_name(volume_name)
        expect(row).to_be_visible(timeout=timeout)

        menu_btn = row.locator('button[data-slot="dropdown-menu-trigger"]').first
        expect(menu_btn).to_be_visible(timeout=timeout)
        expect(menu_btn).to_be_enabled(timeout=timeout)
        menu_btn.click()

    def click_delete_in_menu(self, timeout: int = 10000):
        """row의 dropdown 메뉴에서 '삭제' 메뉴 아이템 클릭"""
        delete_item = self.page.get_by_role("menuitem", name="삭제")
        expect(delete_item).to_be_visible(timeout=timeout)
        delete_item.click()

    def _get_pinned_row_by_name(self, name: str) -> Locator:
        """왼쪽 pinned 영역에서 Volume 이름으로 row 찾기"""
        return self.page.locator(
            ".ag-pinned-left-cols-container [role='row']"
        ).filter(
            has=self.page.get_by_role("link", name=name, exact=True)
        )

    def _get_center_row_by_name(self, name: str) -> Locator:
        """Volume 이름으로 center 영역의 row 찾기"""
        pinned_row = self._get_pinned_row_by_name(name)
        expect(pinned_row).to_have_count(1, timeout=5000)

        # row-index 기준으로 매칭
        row_index = pinned_row.get_attribute("row-index")

        center_row = self.page.locator(
            f".ag-center-cols-container [role='row'][row-index='{row_index}']"
        )
        expect(center_row).to_have_count(1, timeout=5000)

        return center_row

    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_volume(self, desc: str, size: str) -> str:
        volume_name = make_name(prefix="QA-VOLUME-")

        self.fill_form(name=volume_name, desc=desc)
        self.select_option_by_index() # Volume 유형

        self.size_input.fill(size)
        self.select_option_by_index() # 가용 영역 유형
        
        self.submit()

        return volume_name
    
    def delete_volume(self, volume_name: str):
        self.open_row_menu(volume_name)
        self.click_delete_in_menu()
