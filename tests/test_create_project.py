from pages.project_page import ProjectPage

def test_create_project(logged_in_page, log):
    page = logged_in_page

    # 1) 프로젝트 생성
    log.info("프로젝트 생성 시작")
    project_page = ProjectPage(page)
    project_name = project_page.create_project(prefix="TEST_PROJECT_")
    log.info("프로젝트 생성 완료 | 프로젝트 이름=%s", project_name)
