"""
VPC 생성 페이지
"""

from playwright.sync_api import Page, expect
from utils.namer import make_name

class VPCPage:
    def __init__(self, page: Page):
     self.page = page

    def open_vpc_create(self, timeout: int = 10000):
        # VPC 페이지로 이동
        self.page.get_by_role("button", name="VPC", exact=True).click()

        # VPC 생성 버튼 클릭하여 생성 모달 오픈
        self.page.locator("button").filter(has_text="VPC 생성").click()
        expect(self.page.locator('input[name="name"]')).to_be_visible(timeout=timeout)

    def fill_form(self, name: str, cidr: str, timeout: int = 10000):
        self.page.locator('input[name="name"]').click()
        self.page.locator('input[name="name"]').fill(name)

        self.page.get_by_placeholder("VPC CIDR을 입력해주세요").click()
        self.page.locator('input[name="cidr"]').fill(cidr)

    def submit(self, name: str, timeout: int = 20000):
        self.page.get_by_role("button", name="확인").click()

        # VPC 생성 성공 토스트 검증
        expect(self.page.get_by_text("VPC 생성 성공")).to_be_visible(timeout=timeout)

    def create_vpc(self, name_prefix: str = "TEST_VPC", cidr: str = "10.0.0.0/8", timeout: int = 20000) -> str:
        """
        VPC명 랜덤 생성 (예: TEST_VPC_Z9K1)
        """
        vpc_name = make_name(prefix=name_prefix, suffix_len=4)
        self.open_vpc_create(timeout=timeout)
        self.fill_form(name=vpc_name, cidr=cidr, timeout=timeout)
        self.submit(name=vpc_name, timeout=timeout)
        return vpc_name