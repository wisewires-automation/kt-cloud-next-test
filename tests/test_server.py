import time
from pathlib import Path
from utils.playwright_helpers import create_page, login_as_admin, open_project
from utils.logger import get_logger
from utils.capture import ScreenshotSession

from pages.server_page import ServerPage

file_name = Path(__file__).stem
log = get_logger(file_name)

def create_server_scenario(project_opened_page, log, sc: ScreenshotSession | None = None) -> str:
    """
    Server 생성 테스트
    1) Server 메뉴 진입
    2) 서버 이미지 선택
    3) 서버 스펙 선택
    4) 기본 정보 입력 (AZ, 서버 이름)
    5) 네트워크 구성
       - VPC 생성 후 선택
       - Subnet 생성 후 선택
       - NIC 생성 후 선택
    6) Key Pair 생성 후 선택
    7) 서버 생성 버튼 클릭 및 생성 토스트 확인
    """

    page = project_opened_page

    server_page = ServerPage(page)

    log.info("[STEP 0] 서버 생성 페이지 진입")
    server_page.go_server_page()

    log.info("[STEP 1] 서버 이미지 선택 (index=0)")
    server_page.select_server_image(index=0)

    log.info("[STEP 2] 서버 스펙 선택 (index=0)")
    server_page.select_server_spec(index=0)

    log.info("[STEP 3] 서버 기본 정보 입력 (AZ / 서버 이름)")
    server_name = server_page.fill_basic_info()

    log.info("[STEP 4] 스토리지 설정 (Volume 생성 후 선택)")
    # TODO: Volume 생성 후 선택

    log.info("[STEP 5] 네트워크 구성 시작")

    log.info("[STEP 5-1] VPC 생성 및 선택")
    vpc_name = server_page.create_vpc()
    log.info("           - 생성된 VPC 이름: %s", vpc_name)
    server_page.select_vpc_by_name(vpc_name)

    log.info("[STEP 5-2] Subnet 생성 및 선택")
    subnet_name = server_page.create_subnet()
    log.info("           - 생성된 Subnet 이름: %s", subnet_name)
    server_page.select_subnet_by_name(subnet_name)
    sc.snap(page, label="after create subnet")

    log.info("[STEP 5-3] NIC 생성 및 선택")
    nic_name = server_page.create_nic()
    log.info("           - 생성된 NIC 이름: %s", nic_name)
    server_page.select_nic_by_name(nic_name)

    log.info("[STEP 6] 서버 접속용 Key Pair 생성 및 선택")
    kp_name = server_page.creat_kp()
    log.info("         - 생성된 Key Pair 이름: %s", kp_name)
    server_page.select_key_by_name(kp_name)
    sc.snap(page, label="after create key pair")

    log.info("[STEP 7] 서버 생성 요청 및 결과 확인")
    server_page.submit()

    log.info("[DONE] 서버 생성 완료 | 서버 이름: %s", server_name)

    return server_name

def main():
    with create_page(headless=False) as page, \
         ScreenshotSession(__file__, zip_name=file_name) as sc:

        try:
            login_as_admin(page, log)
            open_project(page, log)
            server_name = create_server_scenario(page, log, sc)
            sc.snap(page, label=server_name)
        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] 서버 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()