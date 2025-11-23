""" Floating IP POM """

from playwright.sync_api import Page
from pages.base_page import BasePage

class FIPPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    CREATE_SUCCESS_TEXT = "Floating IP가 성공적으로 생성되었습니다."

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page