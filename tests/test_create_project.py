# from pages.project_page import ProjectPage

# def test_create_project(kt_user, log):
#     """
#     Project 생성 테스트
#     """
#     page = kt_user

#     project_page = ProjectPage(page)

#     log.info("프로젝트 생성 시작")
#     project_name = project_page.create_project(prefix="QA_PROJECT_")

#     log.info("프로젝트 생성 완료 | 프로젝트 이름=%s", project_name)


# tests/test_create_project.py
from scenarios.project_scenarios import create_project_scenario

def test_create_project(kt_logged_in_page, log):
    """
    Project 생성 테스트 (admin 로그인 선행)
    """
    page = kt_logged_in_page
    create_project_scenario(page, log)
