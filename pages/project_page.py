""" Project POM """

import time
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.locators.common import ToastLocators as T, ButtonLocators as B
from pages.locators.actions import CreateButtonLocators as C
from utils.namer import make_name

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
    def create_button(self):
        """모달 - 프로젝트 생성 버튼"""
        return self.page.get_by_role("button", name=B.CREATE_TEXT, exact=True)
    
    @property
    def edit_button(self):
        """프로젝트 수정 버튼"""
        return self.page.get_by_role("button", name=B.EDIT_TEXT)
    
    @property
    def service_in_use_tab(self):
        """'이용중인 서비스' 탭 버튼"""
        return self.page.get_by_role("tab", name=self.SERVICE_IN_USE_TAB)
    
    @property
    def pen_button(self):
        """수정 버튼"""
        return self.page.locator("button:has(span[aria-label='pen'])").first
    
    @property
    def search_all_button(self):
        """'전체 조회' 버튼"""
        return self.page.get_by_label(self.SEARCH_ALL_BUTTON_TEXT)
    
    @property
    def delete_open_button(self):
        """삭제하기 버튼"""
        return self.page.locator(
            "button.s-button--small.s-button--danger"
        ).filter(has_text=B.DELETE_BUTTON_NAME).first

    @property
    def delete_input(self):
        """모달 - 삭제 입력 필드"""
        return self.page.get_by_role("textbox", name="input")

    @property
    def delete_confirm_button(self):
        """모달 - 삭제하기 버튼"""
        return self.page.locator(
            "button.s-button--medium.s-button--danger"
        ).filter(has_text=B.DELETE_BUTTON_NAME).first
    
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

    def fill_form(self, name: str, desc: str = ""):
        """프로젝트 이름, 설명 입력"""
        if name is not None:
            self.name_input.fill(name)

        if desc is not None:
            self.desc_input.fill(desc)

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

    def confirm_delete(self, timeout: int = 10000):
        """
        1) '삭제하기' 버튼 클릭
        2) 인풋에 '삭제' 입력
        3) 최종 삭제 버튼 클릭
        """
        open_btn = self.delete_open_button
        expect(open_btn).to_be_visible(timeout=timeout)
        open_btn.click()

        input = self.delete_input
        expect(input).to_be_visible(timeout=timeout)
        input.fill(B.DELETE_TEXT)

        confirm_btn = self.delete_confirm_button
        expect(confirm_btn).to_be_enabled(timeout=timeout)
        confirm_btn.click()

    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_project(self, desc: str = "qa project 자동 생성",  timeout: int = 20000) -> str:
        """프로젝트 생성"""
        project_name = make_name(prefix="QA-PROJECT-")
        # project_name = "TEST_CREATE_SERVER"

        self.click_project_create()
        self.fill_form(name=project_name, desc=desc, timeout=timeout)
    
        btn = self.create_button
        expect(btn).to_be_enabled(timeout=timeout)
        btn.click()

        """생성 토스트 검증"""
        # self.wait_toast_success_or_fail(success_text=T.CREATE_SUCCESS_TEXT, fail_text=T.CREATE_FAIL_TEXT)
        
        return project_name
    
    def update_project(self, old_name: str, new_name: str, new_desc: str, timeout: int = 10000):
        """프로젝트 수정"""
        self.go_link_by_name(name=old_name)

        time.sleep(1)

        pen_btn = self.pen_button
        expect(pen_btn).to_be_visible(timeout=timeout)
        pen_btn.click()

        self.fill_form(name=new_name, desc=new_desc)

        edit_btn = self.edit_button
        expect(edit_btn).to_be_visible(timeout=timeout)
        edit_btn.click()

        """생성 토스트 검증"""
        # self.wait_toast_success_or_fail(success_text=T.CREATE_SUCCESS_TEXT, fail_text=T.CREATE_FAIL_TEXT)
    
    def delete_project(self, project_name: str):
        """프로젝트 삭제"""
        self.go_link_by_name(name=project_name)
        self.click_service_in_use_tab()
        self.click_search_all()
        time.sleep(2)
        self.confirm_delete()

        """생성 토스트 검증"""
        # self.wait_toast_success_or_fail(success_text=T.DELETE_SUCCESS_TEXT, fail_text=T.DELETE_FAIL_TEXT)
