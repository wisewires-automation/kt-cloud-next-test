import pytest
from playwright.sync_api import sync_playwright
from utils.logger import setup_logging, get_logger

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
