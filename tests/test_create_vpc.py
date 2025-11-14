import os
from dotenv import load_dotenv

from pages.vpc_page import VPCPage

load_dotenv()

def test_create_vpc(project_opened_page, log):
    page = project_opened_page

    # VPC 생성
    log.info("VPC 생성 시작")
    cidr = os.getenv("VPC_CIDR")
    vpc_page = VPCPage(page)
    vpc_name = vpc_page.create_vpc(cidr=cidr)
    log.info("VPC 생성 완료 | VPC 이름=%s", vpc_name)
