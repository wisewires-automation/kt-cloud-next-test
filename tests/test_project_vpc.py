import os
import pytest
import time
from playwright.sync_api import expect
from dotenv import load_dotenv

from pages.auth_page import AuthPage
from pages.project_page import ProjectPage
from pages.vpc_page import VPCPage

load_dotenv()

@pytest.mark.e2e
def test_create_project_then_vpc(page, log):
    """
    테스트 시나리오: 로그인 ➜ 프로젝트 생성 ➜ VPC 생성
    """
    email = os.getenv("KT_EMAIL")
    password = os.getenv("KT_PASSWORD")
    url = os.getenv("KT_LOGIN_URL", "https://console.gcloud.kt.com")

    if not (email and password):
        pytest.skip("환경변수 KT_EMAIL, KT_PASSWORD를 설정해야 실행합니다.")

    # 1) 로그인
    log.info("로그인 시작")
    auth = AuthPage(page)
    auth.login(url=url, email=email, password=password, timeout=15000)
    log.info("로그인 완료")

    time.sleep(3)

    # 프로젝트 생성 및 진입
    log.info("프로젝트 생성 시작")
    project_page = ProjectPage(page)
    project_name = project_page.create_project(prefix="TEST_PROJECT_", description="test project 입니다", timeout=20000)
    log.info("프로젝트 생성 완료 | project_name=%s", project_name)

    # 프로젝트 상세 진입
    # page.get_by_role("link", name="TEST_PROJECT_7S6B").click()

    # 3) VPC 생성
    log.info("VPC 생성 시작 | project=%s", project_name)
    cidr = os.getenv("KT_VPC_CIDR", "10.0.0.0/8")
    vpc_page = VPCPage(page)
    vpc_name = vpc_page.create_vpc(name_prefix="VPC_TEST_", cidr=cidr, timeout=25000)
    log.info("VPC 생성 완료 | vpc_name=%s", vpc_name)