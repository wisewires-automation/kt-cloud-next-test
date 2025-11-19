from playwright.sync_api import Page
from utils.capture import ScreenshotSession
from pages.project_page import ProjectPage

import time

def create_project_scenario(page: Page, log, prefix: str = "QA_P_", sc: ScreenshotSession | None = None) -> str:
    """
    Project 생성 시나리오
    """
    project_page = ProjectPage(page)

    log.info("프로젝트 생성 시작")

    project_name = project_page.create_project(prefix=prefix)
    log.info("프로젝트 생성 완료 | 프로젝트 이름=%s", project_name)

    # 마지막 화면 캡쳐를 위해 추가
    time.sleep(2)

    if sc is not None:
        sc.snap(page, label=project_name)

    return project_name
