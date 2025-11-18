import os
from dotenv import load_dotenv

from pages.vpc_page import VPCPage

load_dotenv()

def test_create_vpc(project_opened_page, log):
    """
    VPC 생성 테스트
    """
    page = project_opened_page

    vpc_page = VPCPage(page)
    
    cidr = os.getenv("CIDR")

    log.info("VPC 생성 팝업 오픈")
    vpc_page.open_vpc_create()
    
    log.info("VPC 생성 시작")
    vpc_name = vpc_page.create_vpc(cidr=cidr)

    log.info("VPC 생성 완료 | VPC 이름=%s", vpc_name)

def test_delete_vpc(project_opened_page, log):
    """
    VPC 삭제 테스트
    """
    page = project_opened_page

    # TODO: VPC 이름 클릭 -> 삭제 버튼 클릭 -> 삭제 가능 여부 판단 -> 삭제 or 삭제 불가능 결과

    vpc_name = ""

    log.info("VPC 삭제 완료 | VPC 이름=%s", vpc_name)