""" Project POM """

import time
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.locators.common import ButtonLocators as B
from pages.locators.actions import CreateButtonLocators as C

class ProjectPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    MANAGE_PROJECT = "프로젝트 관리하기"

    NEW_PROJECT_NAME = "새 프로젝트"
    NAME_INPUT = 'input[name="name"]'           # 프로젝트 이름
    DESC_INPUT = 'input[name="description"]'    # 프로젝트 설명
    
    CREATE_SUCCESS_TEXT = "생성 완료"

    PROEJCT_MEMBER_TAB = "프로젝트 멤버"
    PROJECT_GROUP_TAB = "프로젝트 그룹"
    SERVICE_IN_USE_TAB = "이용중인 서비스"

    SEARCH_ALL_BUTTON_TEXT = "전체 조회"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    # ============================================================
    # PROPERTIES
    # ============================================================    
    @property
    def manage_project_button(self):
        """프로젝트 관리하기 버튼"""
        return self.page.get_by_role("button", name=self.MANAGE_PROJECT, exact=True)
    
    @property
    def create_project_button(self):
        """프로젝트 생성 버튼"""
        return (self.page.locator("button").filter(has_text=C.PROJECT_CREATE).first)
    
    @property
    def new_project(self):
        """'새 프로젝트' 카드"""
        return self.page.get_by_role("heading", name=self.NEW_PROJECT_NAME).first

    @property
    def name_input(self):
        """모달 - 프로젝트 이름 입력 필드"""
        return self.page.locator(self.NAME_INPUT)

    @property
    def desc_input(self):
        """모달 - 프로젝트 설명 입력 필드"""
        return self.page.locator(self.DESC_INPUT)
    
    @property
    def service_in_use_tab(self):
        """'이용중인 서비스' 탭 버튼"""
        return self.page.get_by_role("tab", name=self.SERVICE_IN_USE_TAB)
    
    @property
    def pen_project_button(self):
        """수정 버튼(펜)"""
        return self.page.locator("button:has(span[aria-label='pen'])").first
    
    @property
    def search_all_button(self):
        """'전체 조회' 버튼"""
        return self.page.get_by_label(self.SEARCH_ALL_BUTTON_TEXT)
    
    @property
    def delete_project_button(self):
        """삭제하기 버튼"""
        return self.page.locator("button.s-button--danger", has_text=B.DELETE_BUTTON_NAME)

    @property
    def delete_project_confirm(self):
        """모달 - 삭제하기 버튼"""
        return self.page.locator("button.s-button--medium.s-button--danger").filter(has_text=B.DELETE_BUTTON_NAME).first
    
    # ============================================================
    # ACTIONS
    # ============================================================
    def go_manage_project(self, timeout: int = 10000):
        """프로젝트 관리하기 페이지로 이동"""
        btn = self.manage_project_button
        expect(btn).to_be_visible(timeout=timeout)
        btn.click()

    def click_project_create(self, timeout: int = 10000):
        """프로젝트 생성 모달 열기"""
        btn = self.create_project_button
        expect(btn).to_be_visible(timeout=timeout)
        btn.click()

    def open_create_popup(self, timeout: int = 10000):
        """'새 프로젝트' 카드 클릭하여 생성 모달 열기"""
        try:
            self.new_project.click()
        except Exception:
            self.new_project.scroll_into_view_if_needed(timeout=timeout)
            self.new_project.click()

    def enter_name(self, name):
        """프로젝트 이름 입력"""
        self.name_input.fill(name)

    def enter_desc(self, desc):
        """프로젝트 설명 입력"""
        self.desc_input.fill(desc)

    def fill_form(self, name: str, desc: str):
        """프로젝트 폼 입력"""
        self.enter_name(name)
        self.enter_desc(desc)

    def click_service_in_use_tab(self, timeout: int = 10000):
        """이용중인 서비스 탭 클릭"""
        tab = self.service_in_use_tab
        expect(tab).to_be_visible(timeout=timeout)
        tab.click()

    def click_search_all(self, timeout: int = 10000):
        """이용중인 서비스 탭에서 '전체 조회' 클릭"""
        btn = self.search_all_button
        expect(btn).to_be_visible(timeout=timeout)
        btn.click()

    def click_edit_button(self, timeout: int = 10000):
        """프로젝트 수정 버튼"""
        btn = self.pen_project_button
        expect(btn).to_be_visible(timeout=timeout)
        btn.click()
        
    def delete_confirm(self, timeout: int = 10000):
        """프로젝스 삭제 플로우"""
        open_btn = self.delete_project_button
        expect(open_btn).to_be_visible(timeout=timeout)
        open_btn.click()

        self.enter_delete_text()

        self._safe_click(self.delete_project_confirm, timeout=timeout)

    def open_project(self, project_name: str, timeout: int = 10000):
        """프로젝트 목록에서 특정 프로젝트 진입"""
        link = self.page.get_by_role("link", name=project_name)
        self._safe_click(link, timeout=timeout)

    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_project(self, name: str, desc: str) -> str:
        """프로젝트 생성 플로우"""
        self.open_create_modal(C.PROJECT_CREATE)
        self.fill_form(name, desc)
        self.click_button(text=B.CREATE_TEXT)

        # TODO: 생성 토스트 검증

        return name
    
    def update_project(self, project_name: str, new_name: str, desc: str):
        """프로젝트 수정 플로우"""
        self.go_link_by_name(name=project_name)

        self.click_edit_button()
        self.fill_form(name=new_name, desc=desc)
        self.click_button(text=B.EDIT_TEXT)

        # TODO: 수정 토스트 검증
    
    def delete_project(self, project_name: str):
        """프로젝트 삭제 플로우"""
        # self.go_link_by_name(name=project_name)

        self.click_service_in_use_tab()
        self.click_search_all()

        # 이용중인 서비스 조회 후 대기
        time.sleep(1)
        self.delete_confirm()

        # TODO: 삭제 토스트 검증
