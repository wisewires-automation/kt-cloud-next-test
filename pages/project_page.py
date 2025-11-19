""" Project POM """

import time
from playwright.sync_api import Page, expect
from utils.namer import make_name
from pages.base_page import BasePage
from pages.locators.common import ToastLocators, ButtonLocators

class ProjectPage(BasePage):

    NEW_PROJECT_NAME = "새 프로젝트"

    NAME_INPUT = 'input[name="name"]'           # 프로젝트 이름
    DESC_INPUT = 'input[name="description"]'    # 프로젝트 설명

    CREATE_SUCCESS_TEXT = "생성 완료"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self.new_project = page.get_by_role("heading", name=self.NEW_PROJECT_NAME).first
        self.name_input = page.locator(self.NAME_INPUT)
        self.desc_input = page.locator(self.DESC_INPUT)
        self.create_button = page.get_by_role("button", name=ButtonLocators.CREATE_CONFIRM_BUTTON)

    def open_create_popup(self, timeout: int = 10000):
        """새 프로젝트 카드 클릭하여 프로젝트 생성 모달 오픈"""
        self.page.get_by_role("heading", name="새 프로젝트").first

        # 새 프로젝트 카드 클릭 (실패 시 한 번 더 스크롤 후 재시도)
        try:
            self.new_project.click()
        except Exception:
            self.new_project.scroll_into_view_if_needed(timeout=timeout)
            self.new_project.click()

    def fill_form(self, name: str, description: str = "", timeout: int = 10000):
        expect(self.name_input).to_be_visible(timeout=timeout)
        self.name_input.fill(name)

        # 프로젝트 설명(필수 X)
        if description is not None:
            self.desc_input.fill(description)

    def submit(self):
        self.create_button.click()

    def create_project(self, prefix: str = "QA_PROJECT_", description: str = "test project 자동 생성", timeout: int = 20000) -> str:
        """프로젝트명 랜덤 생성 (예: QA_PROJECT_AB12) 후 생성"""
        project_name = make_name(prefix=prefix)

        self.open_create_popup(timeout=timeout)
        self.fill_form(name=project_name, description=description, timeout=timeout)
        self.submit()

        self.wait_for_toast(ToastLocators.CREATE_SUCCESS_TEXT, timeout=timeout)

        return project_name
    
    def open_project(self, project_name: str, timeout: int = 10000):
        link = self.page.get_by_role("link", name=project_name)
        
        expect(link).to_be_visible(timeout=timeout)
        link.click()

        time.sleep(3)