from pages.sg_page import SGPage

def test_create_sg(project_opened_page, log):
    """
    Security Groups 생성 테스트
    """
    page = project_opened_page

    sg_page = SGPage(page)

    log.info("Security Groups 생성 팝업 오픈")
    sg_page.open_sg_create()

    log.info("Security Groups 생성 시작")
    sg_name = sg_page.create_sg()

    log.info("Security Groups 생성 완료 | Security Groups 이름=%s", sg_name)
