from pages.nic_page import NICPage

def test_create_nic(project_opened_page, log):
    page = project_opened_page

    nic_page = NICPage(page)

    log.info("NIC 생성 팝업 오픈")
    nic_page.open_nic_create()

    log.info("NIC 생성 시작")
    nic_name = nic_page.create_nic()
    log.info("NIC 생성 완료 | NIC 이름=%s", nic_name)
