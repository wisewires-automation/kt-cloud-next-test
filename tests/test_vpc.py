import os
from dotenv import load_dotenv
from playwright.sync_api import Page
from pathlib import Path
from utils.playwright_helpers import create_page, login_as_admin
from utils.logger import get_logger
from utils.capture import ScreenshotSession

from pages.vpc_page import VPCPage

load_dotenv()

file_name = Path(__file__).stem
log = get_logger(file_name)

def create_vpc_scenario(page: Page, log, sc: ScreenshotSession | None = None) -> str:
    """
    VPC 생성 테스트
    """
    vpc_page = VPCPage(page)
    
    cidr = os.getenv("CIDR")

    log.info("VPC 생성 팝업 오픈")
    vpc_page.open_vpc_create()
    
    log.info("VPC 생성 시작")
    vpc_name = vpc_page.create_vpc(cidr=cidr)

    log.info("VPC 생성 완료 | VPC 이름=%s", vpc_name)

    return vpc_name

def main():
    with create_page(headless=False) as page, ScreenshotSession(__file__, zip_name=file_name) as sc:

        try:
            login_as_admin(page, log)
            vpc_name = create_vpc_scenario(page, log, sc)
            sc.snap(page, label=vpc_name)
        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] VPC 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()