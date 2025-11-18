from pages.kp_page import KPPage

def test_create_kp(project_opened_page, log):
    """
    Key Pair 생성 테스트
    """
    page = project_opened_page

    kp_page = KPPage(page)

    log.info("Key Pair 생성 팝업 오픈")
    kp_page.open_kp_create()

    log.info("Key Pair 생성 시작")
    kp_name = kp_page.create_kp()

    log.info("Key Pair 생성 완료 | Key Pair 이름=%s", kp_name)
