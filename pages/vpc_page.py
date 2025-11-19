""" VPC POM """

from playwright.sync_api import Page, expect
from pages.locators.actions import SidebarLocators as S, CreateButtonLocators as C
from pages.locators.common import ToastLocators as T, ButtonLocators as B
from utils.namer import make_name

class VPCPage:

    NAME_INPUT = 'input[name="name"]'   # VPC 이름
    CIDR_INPUT = 'input[name="cidr"]'   # CIDR 주소

    CREATE_SUCCESS_TEXT = "VPC 생성 성공"

    def __init__(self, page: Page):
        self.page = page

        self.vpc_nav_button = page.get_by_role("button", name=S.VPC_MENU, exact=True)
        self.vpc_create_button = (page.locator("button").filter(has_text=C.VPC_CREATE).first)
        self.name_input = page.locator(self.NAME_INPUT)
        self.cidr_input = page.locator(self.CIDR_INPUT)
        self.confirm_button = page.get_by_role("button",name=B.CONFIRM_BUTTON)

    def open_vpc_create(self, timeout: int = 10000):
        expect(self.vpc_nav_button).to_be_visible(timeout=timeout)
        self.vpc_nav_button.click()

        expect(self.vpc_create_button).to_be_visible(timeout=timeout)
        self.vpc_create_button.click()

    def fill_form(self, name: str, cidr: str, timeout: int = 10000):
        expect(self.name_input).to_be_visible(timeout=timeout)
        self.name_input.fill(name)

        expect(self.cidr_input).to_be_visible(timeout=timeout)
        self.cidr_input.fill(cidr)

    def submit(self, timeout: int = 20000):
        expect(self.confirm_button).to_be_enabled(timeout=timeout)
        self.confirm_button.click()

        expect(self.page.get_by_text(self.CREATE_SUCCESS_TEXT)).to_be_visible(timeout=timeout)

    def create_vpc(self, name_prefix: str = "QA-VPC", cidr: str = "10.0.0.0/8") -> str:
        vpc_name = make_name(prefix=name_prefix)
        
        self.fill_form(name=vpc_name, cidr=cidr)
        self.submit()

        return vpc_name