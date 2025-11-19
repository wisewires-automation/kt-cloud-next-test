import os
from dotenv import load_dotenv
from playwright.sync_api import Page
from pathlib import Path
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.capture import ScreenshotSession

from pages.subnet_page import SubnetPage

load_dotenv()

file_name = Path(__file__).stem
log = get_logger(file_name)

def create_subnet_scenario(page: Page, log, sc: ScreenshotSession | None = None) -> str:
    """
    Subnet 생성 테스트
    - 대상 프로젝트 내에 VPC가 생성되어 있어야 함
    """
    subnet_page = SubnetPage(page)

    cidr = os.getenv("CIDR")

    log.info("Subnet 생성 팝업 오픈")
    subnet_page.open_subnet_create()
    
    log.info("Subnet 생성 시작")
    subnet_name = subnet_page.create_subnet(cidr=cidr)
    
    log.info("Subnet 생성 완료 | Subnet 이름=%s", subnet_name)

    return subnet_name

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:

        try:
            login_as_admin(page, log)
            subnet_name = create_subnet_scenario(page, log, sc)
            sc.snap(page, label=subnet_name)
        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] Subnet 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()