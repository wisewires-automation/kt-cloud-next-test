import pytest, os, time
from playwright.sync_api import sync_playwright
from utils.logger import setup_logging, get_logger
from dotenv import load_dotenv

from pages.auth_page import AuthPage
from pages.project_page import ProjectPage

load_dotenv()
setup_logging()

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="function")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture(scope="function")
def log(request):
    # 각 테스트 이름을 컨텍스트로 넣어줌
    return get_logger(request.node.name)


@pytest.fixture
def logged_in_page(page, log):
    """로그인된 상태의 fixture"""
    url   = os.getenv("LOGIN_URL")
    kt_id = os.getenv("KT_USER_ID")
    kt_pw = os.getenv("KT_USER_PW")

    if not (url and kt_id and kt_pw):
        pytest.skip("LOGIN_URL, KT_USER_ID, KT_USER_PW 환경변수 설정 필요")

    auth = AuthPage(page)

    log.info("[KT] 로그인 시작")
    auth.login_kt(url=url, user_id=kt_id, password=kt_pw)
    log.info("[KT] 로그인 완료")

    time.sleep(2)

    return page

@pytest.fixture
def project_name():
    return os.getenv("PROJECT_NAME", "TEST_CREATE_SERVER")

@pytest.fixture
def project_opened_page(logged_in_page, project_name, log):
    """로그인 + 프로젝트 진입 fixture"""
    page = logged_in_page
    project_page = ProjectPage(page)

    log.info("프로젝트 진입 | 프로젝트 이름=%s", project_name)
    project_page.open_project(project_name)

    return page