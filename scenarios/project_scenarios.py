from playwright.sync_api import Page
from pages.project_page import ProjectPage

def create_project_scenario(page: Page, log, prefix: str = "QA_PROJECT_") -> str:
    """
    공통 Project 생성 시나리오
    - pytest 테스트에서도 쓰고
    - python 단독 실행 스크립트에서도 재사용
    """
    project_page = ProjectPage(page)

    log.info("프로젝트 생성 시작")
    project_name = project_page.create_project(prefix=prefix)
    log.info("프로젝트 생성 완료 | 프로젝트 이름=%s", project_name)

    return project_name
