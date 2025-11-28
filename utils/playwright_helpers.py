"""
playwright_helpers.py

Playwright 기반 테스트에서 자주 쓰이는 공통 액션/유틸 함수 모음.

- 브라우저 / 페이지 생성용 context manager
- admin / IAM 계정 로그인
- 특정 프로젝트 진입
"""

import os
import time
from contextlib import contextmanager
from typing import Optional, Iterator, ContextManager
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Page
from utils.logger import setup_logging, get_logger
from pages.auth_page import AuthPage
from pages.project_page import ProjectPage

load_dotenv()
setup_logging()

def create_page(headless: bool = False) -> ContextManager[Page]:
    """
    Playwright 브라우저/페이지를 생성해 주는 context manager 반환 헬퍼.

    사용 예시:
        from playwright_helpers import create_page

        with create_page(headless=True) as page:
            login_as_admin(page)
            open_project(page, project_name="QA_TEST_PROJECT")

    Args:
        headless (bool): 헤드리스 모드 여부 (기본 False)
    """

    @contextmanager
    def _cm() -> Iterator[Page]:
        # Playwright 런타임 시작
        with sync_playwright() as p:
            # Chromium 브라우저 실행
            browser = p.chromium.launch(headless=headless)
            # 새 브라우저 컨텍스트 및 페이지 생성
            context = browser.new_context()
            page = context.new_page()

            try:
                # with 블록 내부로 Page 객체 넘겨줌
                yield page
            finally:
                # with 블록 종료 시 자원 정리
                context.close()
                browser.close()

    return _cm()

def login_as_admin(page: Page, log: Optional[object]) -> Page:
    """
    admin 계정으로 로그인하는 공통 헬퍼.

    환경변수:
        - LOGIN_URL : 로그인 페이지 URL
        - KT_USER_ID: admin 계정 ID
        - KT_USER_PW: admin 계정 PW

    Args:
        page: Playwright 페이지 객체
        log: 외부에서 주입한 로거. 미지정 시 "login_as_admin" 로거 사용

    Returns:
        Page: 로그인 완료 후의 동일 Page 객체
    """
    # 외부에서 로거를 넘기지 않으면 기본 로거 사용
    log = log or get_logger("login_as_admin")

    url     = os.getenv("LOGIN_URL")
    user_id = os.getenv("KT_USER_ID")
    user_pw = os.getenv("KT_USER_PW")

    # 환경 변수 체크
    if not (url and user_id and user_pw):
        raise RuntimeError("LOGIN_URL, KT_USER_ID, KT_USER_PW 환경변수 설정 필요")

    auth = AuthPage(page)

    log.info("[ADMIN] 로그인 시작")
    auth.login_admin(url, user_id, user_pw)
    log.info("[ADMIN] 로그인 완료")

    # 로그인 이후 페이지 로딩/리다이렉트 안정화를 위한 짧은 대기
    time.sleep(2)

    return page


def login_as_iam(page: Page, log: Optional[object], user_id: str = "") -> Page:
    """
    IAM 계정으로 로그인하는 공통 헬퍼.

    Args:
        page: Playwright 페이지 객체
        log: 외부에서 주입한 로거. 미지정 시 "login_as_iam" 로거 사용
        user_id: 로그인하려는 IAM 계정 ID (로그 출력용)

    Returns:
        Page: 로그인 완료 후의 동일 Page 객체
    """
    log = log or get_logger("login_as_iam")

    url         = os.getenv("LOGIN_URL")
    group_id    = os.getenv("GROUP_ID")
    user_id     = os.getenv("IAM_USER_ID")
    user_pw     = os.getenv("IAM_USER_PW")

    # 환경 변수 체크
    if not (url and group_id and user_id and user_pw):
        raise RuntimeError("LOGIN_URL, GROUP_ID, IAM_USER_ID, IAM_USER_PW 환경변수 설정 필요")

    auth = AuthPage(page)

    log.info("[IAM] 로그인 시작 | 아이디=%s", user_id)

    # TODO: IAM 로그인 방식 확정 후 실제 구현 추가
    auth.login_iam(url, group_id, user_id, user_pw)

    log.info("[IAM] 로그인 완료")

    return page


# def open_project(page: Page, log: Optional[object], project_name: str = "QA-AUTO-PROJECT") -> Page:
#     """프로젝트 목록에서 지정한 프로젝트로 진입하는 헬퍼"""
#     log = log or get_logger("open_project")

#     project_page = ProjectPage(page)

#     log.info("프로젝트 진입 시도 | 프로젝트 이름=%s", project_name)
#     project_page.open_project(project_name)
#     log.info("프로젝트 진입 완료")

#     return page



