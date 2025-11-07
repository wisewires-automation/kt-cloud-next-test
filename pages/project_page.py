"""
프로젝트 생성 페이지
"""

from playwright.sync_api import Page, expect
from utils.namer import make_name

class ProjectPage:
    def __init__(self, page: Page):
        self.page = page

    def open_create_popup(self, timeout: int = 10000):
        # 새 프로젝트 클릭하여 프로젝스 생성 모달 오픈
        heading = self.page.get_by_role("heading", name="새 프로젝트").first

        # 새 프로젝트 카드가 보일때까지 스크롤
        heading.scroll_into_view_if_needed(timeout=timeout)

        # 새 프로젝트 카드 노출 확인
        expect(heading).to_be_visible(timeout=timeout)

        # 새 프로젝트 카드 클릭 (실패 시 한 번 더 스크롤 후 재시도)
        try:
            heading.click()
        except Exception:
            heading.scroll_into_view_if_needed(timeout=timeout)
            heading.click()

        # 프로젝트명 입력란이 보일 때까지 대기
        expect(self.page.locator('input[name="name"]')).to_be_visible(timeout=timeout)


    def fill_form(self, name: str, description: str = "", timeout: int = 10000):
        self.page.locator('input[name="name"]').click()
        self.page.locator('input[name="name"]').fill(name)

        # 프로젝트 설명 필수 X
        if description is not None:
            self.page.locator('input[name="description"]').click()
            self.page.locator('input[name="description"]').fill(description)

    def submit(self, timeout: int = 20000):
        self.page.get_by_role("button", name="생성").click()

        # 프로젝트 생성 성공 토스트 검증
        expect(self.page.get_by_text("생성 완료")).to_be_visible(timeout=timeout)


    def create_project(self, prefix: str = "TEST_PROJECT_", description: str = "test project 자동 생성", timeout: int = 20000) -> str:
        """
        프로젝트명 랜덤 생성 (예: TEST_PROJECT_AB12)
        """
        project_name = make_name(prefix=prefix, suffix_len=4)
        self.open_create_popup(timeout=timeout)
        self.fill_form(name=project_name, description=description, timeout=timeout)
        self.submit(timeout=timeout)
        return project_name