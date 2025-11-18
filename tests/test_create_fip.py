from pages.fip_page import FIPPage
import time

def test_create_fip(project_opened_page, log):
    """
    Floating IP 생성 테스트
    """
    page = project_opened_page

    fip_page = FIPPage(page)

    log.info("Floating IP 생성 팝업 오픈")
    fip_page.open_fip_create()

    log.info("Floating IP 생성")
    fip_page.submit()
    
    time.sleep(3)

    log.info("Floating IP 생성 완료")
