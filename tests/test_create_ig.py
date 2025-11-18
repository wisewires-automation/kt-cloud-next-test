from pages.ig_page import IGPage

def test_create_ig(project_opened_page, log):
    """
    Internet Gateway 생성 테스트
    """
    page = project_opened_page

    ig_page = IGPage(page)

    log.info("Internet Gateway 생성 팝업 오픈")
    ig_page.open_ig_create()

    log.info("Internet Gateway 생성 시작")
    ig_name = ig_page.create_ig()

    log.info("Internet Gateway 생성 완료 | Internet Gateway 이름=%s", ig_name)
