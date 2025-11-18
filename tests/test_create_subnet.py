import os
from dotenv import load_dotenv

from pages.subnet_page import SubnetPage

load_dotenv()

def test_create_subnet(project_opened_page, log):
    """
    Subnet 생성 테스트
    - 대상 프로젝트 내에 VPC가 생성되어 있어야 함
    """
    page = project_opened_page

    subnet_page = SubnetPage(page)

    cidr = os.getenv("CIDR")

    log.info("Subnet 생성 팝업 오픈")
    subnet_page.open_subnet_create()
    
    log.info("Subnet 생성 시작")
    subnet_name = subnet_page.create_subnet(cidr=cidr)
    
    log.info("Subnet 생성 완료 | Subnet 이름=%s", subnet_name)
