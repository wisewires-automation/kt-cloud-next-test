""" Project POM """

from playwright.sync_api import Page, expect
from utils.namer import make_name
import time

class ProjectPage:

    # ===== selector / text 상수 =====
    NEW_PROJECT_HEADING_NAME = "새 프로젝트"

    PROJECT_NAME_INPUT = 'input[name="name"]'           # 프로젝트 이름
    PROJECT_DESC_INPUT = 'input[name="description"]'    # 프로젝트 설명

    CREATE_BUTTON_NAME = "생성"
    CREATE_SUCCESS_TEXT = "생성 완료"

    def __init__(self, page: Page):
        self.page = page

        # 새 프로젝트 카드 헤딩
        self.new_project_heading = page.get_by_role("heading", name=self.NEW_PROJECT_HEADING_NAME).first

        # 폼 입력 필드
        self.name_input = page.locator(self.PROJECT_NAME_INPUT)
        self.desc_input = page.locator(self.PROJECT_DESC_INPUT)

        # 생성 버튼
        self.create_button = page.get_by_role("button", name=self.CREATE_BUTTON_NAME)

    # ===== 공통 동작 =====
    def open_create_popup(self, timeout: int = 10000):
        """새 프로젝트 카드 클릭하여 프로젝트 생성 모달 오픈"""
        self.page.get_by_role("heading", name="새 프로젝트").first

        # 새 프로젝트 카드 클릭 (실패 시 한 번 더 스크롤 후 재시도)
        try:
            self.new_project_heading.click()
        except Exception:
            self.new_project_heading.scroll_into_view_if_needed(timeout=timeout)
            self.new_project_heading.click()

        # 프로젝트명 입력란이 보일 때까지 대기
        expect(self.name_input).to_be_visible(timeout=timeout)

    def fill_form(self, name: str, description: str = "", timeout: int = 10000):
        self.name_input.fill(name)

        # 프로젝트 설명(필수 X)
        if description is not None:
            self.desc_input.fill(description)

    def submit(self):
        """생성 버튼 클릭"""
        self.create_button.click()

    def create_project(self, prefix: str = "TEST_PROJECT_", description: str = "test project 자동 생성", timeout: int = 20000) -> str:
        """프로젝트명 랜덤 생성 (예: TEST_PROJECT_AB12) 후 생성"""
        # project_name = make_name(prefix=prefix)
        project_name = "QA_TEST_PROJECT"

        self.open_create_popup(timeout=timeout)
        time.sleep(3)
        self.fill_form(name=project_name, description=description, timeout=timeout)
        time.sleep(3)
        self.submit()

        # 프로젝트 생성 성공 토스트 검증
        expect(self.page.get_by_text(self.CREATE_SUCCESS_TEXT)).to_be_visible(timeout=timeout)

        return project_name
    
    def open_project(self, project_name: str, timeout: int = 10000):
        link = self.page.get_by_role("link", name=project_name)
        expect(link).to_be_visible(timeout=timeout)
        link.click()
        time.sleep(3)