import os
from dotenv import load_dotenv

from pages.subnet_page import SubnetPage

load_dotenv()

def test_create_subnet(project_opened_page, log):
    page = project_opened_page

    # Subnet 생성
    log.info("Subnet 생성 시작")
    cidr = os.getenv("SUBNET_CIDR")
    subnet_page = SubnetPage(page)
    subnet_name = subnet_page.create_vpc(cidr=cidr)
    log.info("Subnet 생성 완료 | Subnet 이름=%s", subnet_name)
