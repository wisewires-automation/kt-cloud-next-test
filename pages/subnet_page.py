from playwright.sync_api import Page, expect
from utils.namer import make_name

class SubnetPage:

    # ===== selector / text 상수 =====
    SUBNET_NAV_BUTTON_NAME = "Subnet"
    SUBNET_CREATE_BUTTON_NAME = "Subnet 생성"

    SUBNET_NAME_INPUT = 'input[name="name"]' # Subnet 이름
    SUBNET_CIDR_INPUT = 'input[name="cidr"]' # Subnet CIDR 블록
    SUBNET_SELECT_NAME = "VPC를 선택해주세요" # VPC 선택이름

    CONFIRM_BUTTON_NAME = "확인"
    
    SUBNET_CREATE_SUCCESS_TEXT = "Subnet 생성 성공"
    SUBNET_CREATE_FAIL_TEXT = "생성 실패"

    def __init__(self, page: Page):
        self.page = page

        self.subnet_nav_button = page.get_by_role("button", name=self.SUBNET_NAV_BUTTON_NAME, exact=True)
        self.subnet_create_button = (page.locator("button").filter(has_text=self.SUBNET_CREATE_BUTTON_NAME).first)

        self.name_input = page.locator(self.SUBNET_NAME_INPUT)
        self.cidr_input = page.locator(self.SUBNET_CIDR_INPUT)
        self.vpc_select = (self.page.get_by_role("combobox").filter(has_text=self.SUBNET_SELECT_NAME).first)
        self.vpc_options = self.page.locator(".s-select-options-container .s-select-item--option")

        self.confirm_button = page.get_by_role("button", name=self.CONFIRM_BUTTON_NAME)

    # ===== 공통 동작 =====
    def open_subnet_create(self, timeout: int = 10000):
        expect(self.subnet_nav_button).to_be_visible(timeout=timeout)
        self.subnet_nav_button.click()

        expect(self.subnet_create_button).to_be_visible(timeout=timeout)
        self.subnet_create_button.click()

    def select_vpc_option_by_index(self, idx: int = 0):
        self.vpc_select.click()
        self.vpc_options.nth(idx).click()

    def fill_form(self, name: str, cidr: str):
        self.name_input.fill(name)
        self.cidr_input.fill(cidr)

    def submit(self, timeout: int = 10000):
        expect(self.confirm_button).to_be_enabled(timeout=timeout)
        self.confirm_button.click()

        """Subnet 생성 토스트 검증"""
        success_toast = self.page.get_by_text(self.SUBNET_CREATE_SUCCESS_TEXT)
        fail_toast = self.page.get_by_text(self.SUBNET_CREATE_FAIL_TEXT)
        
        try:
            # 1차: 성공 토스트 대기
            expect(success_toast).to_be_visible(timeout=timeout)
        except Exception:
            # 2차: 실패 토스트 확인
            try:
                expect(fail_toast).to_be_visible(timeout=timeout)
                raise AssertionError("Subnet 생성 실패")
            except Exception:
                raise

    def create_vpc(self, name_prefix: str = "SUBNET-", cidr: str = "10.0.0.0/8") -> str:
        subnet_name = make_name(prefix=name_prefix, suffix_len=4)

        self.open_subnet_create()
        self.select_vpc_option_by_index(idx=2)
        self.fill_form(name=subnet_name, cidr=cidr)
        self.submit()
        return subnet_name