from pages.server_page import ServerPage
from pages.nic_page import NICPage
import time

def test_create_server(project_opened_page, log):
    page = project_opened_page

    server_page = ServerPage(page)
    nic_page = NICPage(page)

    log.info("서버 페이지 진입")
    server_page.go_server_page()

    log.info("01. 서버 이미지 선택")
    server_page.select_server_image(index=0)

    log.info("02. 서버 스펙 선택")
    server_page.select_server_spec(index=0)

    log.info("03. 서버 기본 정보")
    server_name = server_page.fill_basic_info()

    log.info("04. 스토리지 설정")

    log.info("05. 네트워크 구성")
    server_page.select_vpc_option_by_index()
    server_page.select_subnet_option_by_index()
    server_page.select_nic()

    log.info("06. 서버 접속 및 초기 설정")
    server_page.select_kp_option(index=1)

    log.info("서버 생성 완료 | 서버 이름=%s", server_name)
    server_page.submit()