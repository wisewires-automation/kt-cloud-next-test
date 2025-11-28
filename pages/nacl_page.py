""" Network ACL POM """

from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.common import ButtonLocators as B
from pages.actions import CreateButtonLocators as C
from utils.name_generator import generate_name

class ACLPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    NAME_INPUT = 'input[name="name"]'        # 네트워크 ACL 이름
    DESC_INPUT = 'input[name="description"]' # 네트워크 ACL 설명

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    # ============================================================
    # PROPERTIES
    # ============================================================ 
    @property
    def name_input(self):
        """모달 - VPC 이름 입력 필드"""
        return self.page.locator(self.NAME_INPUT)

    @property
    def desc_input(self):
        """모달 - 설명 입력 필드"""
        return self.page.locator(self.DESC_INPUT)
    
    @property
    def edit_confirm_button(self):
        """모달 - 수정 버튼"""
        dialog = self._get_dialog()
        return dialog.locator('button[aria-label="수정"]').first

    # ============================================================
    # ACTIONS
    # ============================================================
    def enter_name(self, name: str): 
        """Network ACL 이름입력"""
        self.name_input.fill(name)

    def enter_desc(self, desc: str): 
        """Network ACL 설명 입력"""
        self.desc_input.fill(desc)

    def fill_form(self, name: str, desc: str):
        """네트워크 ACL 폼 입력"""
        self.enter_name(name)
        self.enter_desc(desc)
        
    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_nacl(self, desc: str = "") -> str:
        """Network ACL 생성 플로우"""
        nacl_name = generate_name(prefix="QA-NACL-")

        self.open_create_modal(C.NACL_CREATE)
        self.fill_form(name=nacl_name, desc=desc)
        self.click_button(text=B.CREATE_BUTTON_NAME)
        
        return nacl_name
    
    def update_nacl(self, nacl_name: str, new_name: str, desc: str = ""):
        """Network ACL 수정 플로우"""
        self.go_link_by_name(name=nacl_name)
        self.open_modal(text="수정")
        self.fill_form(name=new_name, desc=desc)
        self._safe_click(self.edit_confirm_button)
    
    def delete_nacl(self, nacl_name: str):
        """Network ACL 삭제 플로우"""
        # self.go_link_by_name(name=nacl_name)
        self.open_delete_modal()
        self.run_delete_flow()