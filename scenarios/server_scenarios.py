import time
from playwright.sync_api import Page
from pages.server_page import ServerPage
from pages.nic_page import NICPage

def create_server_scenario(page: Page, log, project_already_open: bool = True) -> str:
    """
    Server 생성 통합 시나리오
    - 전제: 로그인 및 대상 프로젝트 진입까지 완료된 페이지(page)를 인자로 받음
    - 리턴: 생성된 서버 이름
    """

    server_page = ServerPage(page)
    nic_page = NICPage(page)  # 현재는 server_page에서 NIC 관련 동작을 호출한다면, 필요시만 사용

    log.info("[STEP 0] 서버 생성 페이지 진입")
    server_page.go_server_page()
    time.sleep(3)

    log.info("[STEP 1] 서버 이미지 선택 (index=0)")
    server_page.select_server_image(index=0)
    time.sleep(3)

    log.info("[STEP 2] 서버 스펙 선택 (index=0)")
    server_page.select_server_spec(index=0)
    time.sleep(3)

    log.info("[STEP 3] 서버 기본 정보 입력 (AZ / 서버 이름)")
    server_name = server_page.fill_basic_info()
    time.sleep(3)

    log.info("[STEP 4] 스토리지 설정 (Volume 생성 후 선택 예정)")
    # TODO: Volume 생성 후 선택 로직 추가 예정

    log.info("[STEP 5] 네트워크 구성 시작")

    log.info("[STEP 5-1] VPC 생성 및 선택")
    vpc_name = server_page.create_vpc()
    log.info("           - 생성된 VPC 이름: %s", vpc_name)
    server_page.select_vpc_by_name(vpc_name)
    time.sleep(3)

    log.info("[STEP 5-2] Subnet 생성 및 선택")
    subnet_name = server_page.create_subnet()
    log.info("           - 생성된 Subnet 이름: %s", subnet_name)
    server_page.select_subnet_by_name(subnet_name)
    time.sleep(3)

    log.info("[STEP 5-3] NIC 생성 및 선택")
    nic_name = server_page.create_nic()
    log.info("           - 생성된 NIC 이름: %s", nic_name)
    server_page.select_nic_by_name(nic_name)
    time.sleep(3)

    log.info("[STEP 6] 서버 접속용 Key Pair 생성 및 선택")
    kp_name = server_page.creat_kp()
    log.info("         - 생성된 Key Pair 이름: %s", kp_name)
    server_page.select_key_by_name(kp_name)
    time.sleep(3)

    log.info("[STEP 7] 서버 생성 요청 및 결과 확인")
    server_page.submit()
    time.sleep(3)

    log.info("[DONE] 서버 생성 완료 | 서버 이름: %s", server_name)
    return server_name
