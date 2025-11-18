from pages.rt_page import RTPage

def test_create_rt(project_opened_page, log):
    """
    Route Table 생성 테스트
    - 대상 프로젝트 내에 VPC가 생성되어 있어야 함
    """
    page = project_opened_page

    rt_page = RTPage(page)

    log.info("Route Table 생성 팝업 오픈")
    rt_page.open_rt_create()

    log.info("Route Table 생성 시작")
    rt_name = rt_page.create_rt()

    log.info("Route Table 생성 완료 | Route Table 이름=%s", rt_name)
