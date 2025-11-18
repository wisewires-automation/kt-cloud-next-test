import pytest, os, time, json
from playwright.sync_api import sync_playwright
from utils.logger import setup_logging, get_logger
from dotenv import load_dotenv

from pages.auth_page import AuthPage
from pages.user_page import UserPage
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

@pytest.fixture
def log(request):
    # 각 테스트 이름을 컨텍스트로 넣어줌
    return get_logger(request.node.name)


@pytest.fixture(scope="session")
def iam_users():
    """여러 권한의 IAM 유저 정보 목록"""
    with open("config/iam_project_role.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
@pytest.fixture
def iam_user_info(iam_users):
    return iam_users["TEMP"]

@pytest.fixture
def kt_logged_in_page(page, log):
    """
    KT cloud (admin 계정)으로 로그인된 상태 fixture
    """
    url   = os.getenv("LOGIN_URL")
    kt_id = os.getenv("KT_USER_ID")
    kt_pw = os.getenv("KT_USER_PW")

    if not (url and kt_id and kt_pw):
        pytest.skip("LOGIN_URL, KT_USER_ID, KT_USER_PW 환경변수 설정 필요")

    auth = AuthPage(page)

    log.info("[ADMIN] 로그인 시작")
    auth.login_kt(url=url, user_id=kt_id, password=kt_pw)
    log.info("[ADMIN] 로그인 완료")

    time.sleep(2)
    return page

@pytest.fixture
def iam_logged_in_page(page, iam_user_info, log):
    """
    IAM 계정으로 로그인된 상태의 fixture
    """
    login_url = os.getenv("LOGIN_URL")
    group_id  = os.getenv("GROUP_ID")

    auth_page = AuthPage(page)

    log.info("[IAM] 로그인 시작 | id=%s", iam_user_info["id"])
    auth_page.login_iam(
        url=login_url,
        group_id=group_id,
        user_id=iam_user_info["id"],
        password=iam_user_info["password"],
    )
    log.info("[IAM] 로그인 완료 | id=%s", iam_user_info["id"])

    return page

@pytest.fixture
def project_opened_page(kt_logged_in_page, log):
    """
    로그인 + 프로젝트 진입 fixture
    """
    page = kt_logged_in_page
    # page = iam_logged_in_page
    # print('iam_user_info :', iam_user_info)

    project_page = ProjectPage(page)

    project_name = "TEST_CREATE_SERVER"

    log.info("프로젝트 진입 | 프로젝트 이름=%s", project_name)
    project_page.open_project(project_name)

    return page