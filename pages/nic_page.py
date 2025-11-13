from playwright.sync_api import Page, expect

class NICPage:

    # ===== selector / text 상수 =====
    NIC_NAV_BUTTON_NAME = "NIC (Network Interface)"
    NIC_CREATE_BUTTON_NAME = "NIC 생성"

    NIC_NAME_INPUT = 'input[name="name"]' # NIC 이름
    NIC_IP_INPUT = 'input[name="ipAddress"]' # 사설 IP

    CONFIRM_BUTTON_NAME = "확인"
    NIC_CREATE_SUCCESS_TEXT = "생성 완료"

    def __init__(self, page: Page):
        self.page = page

        self.vpc_nav_button = page.get_by_role("button", name=self.NIC_NAV_BUTTON_NAME, exact=True)
        self.vpc_create_button = (page.locator("button").filter(has_text=self.NIC_CREATE_BUTTON_NAME).first)

        self.name_input = page.locator(self.NIC_NAME_INPUT)

        self.confirm_button = page.get_by_role("button",name=self.CONFIRM_BUTTON_NAME)

    # ===== 공통 동작 =====
    def open_vpc_create(self, timeout: int = 10000):
        """VPC 메뉴 이동 후 'VPC 생성' 모달 오픈"""
        expect(self.vpc_nav_button).to_be_visible(timeout=timeout)
        self.vpc_nav_button.click()

        expect(self.vpc_create_button).to_be_visible(timeout=timeout)
        self.vpc_create_button.click()

    def fill_form(self, name: str, cidr: str, timeout: int = 10000):
        expect(self.name_input).to_be_visible(timeout=timeout)
        self.name_input.fill(name)

        expect(self.cidr_input).to_be_visible(timeout=timeout)
        self.cidr_input.fill(cidr)

    def submit(self, name: str, timeout: int = 20000):
        expect(self.confirm_button).to_be_enabled(timeout=timeout)
        self.confirm_button.click()

        """VPC 생성 성공 토스트 검증"""
        expect(self.page.get_by_text(self.VPC_CREATE_SUCCESS_TEXT)).to_be_visible(timeout=timeout)

    def create_vpc(self, name_prefix: str = "TEST_VPC", cidr: str = "10.0.0.0/8", timeout: int = 20000) -> str:
        """VPC명 랜덤 생성 (예: TEST_VPC_Z9K1)"""
        vpc_name = make_name(prefix=name_prefix, suffix_len=4)

        self.open_vpc_create(timeout=timeout)
        self.fill_form(name=vpc_name, cidr=cidr, timeout=timeout)
        self.submit(name=vpc_name, timeout=timeout)
        return vpc_name