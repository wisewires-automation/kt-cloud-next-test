""" Security Group POM """

import time
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from pages.actions import CreateButtonLocators as C
from pages.common import ButtonLocators as B

class SGPage(BasePage):
    # ============================================================
    # TEXT / SELECTOR (텍스트 & 셀렉터 상수)
    # ============================================================
    NAME_INPUT = 'input[name="name"]'        # Security Group 이름 입력 필드
    DESC_INPUT = 'input[name="description"]' # Security Group 설명 입력 필드
    
    IP_PROTOCAL_LABEL = "IP 프로토콜"
    PORT_RANGE_LABEL = "포트 범위"
    REMOTE_LABEL = "원격"

    # IP 프로토콜
    ALL_PROTOCOL = "All 프로토콜"    
    ALL_TCP      = "All TCP"    
    ALL_UDP      = "All UDP"    
    ALL_ICMP     = "All ICMP"    
    CUSTOM_TCP   = "사용자정의 TCP"    
    CUSTOM_UDP   = "사용자정의 UDP"    
    CUSTOM_ICMP  = "사용자정의 ICMP"    

    # 원격
    CIDR = "CIDR"
    SECURITY_GROUP ="보안 그룹"

    # 포트 범위
    PORT_UNIT  = "단일 포트"
    PORT_RANGE = "범위 포트"

    ADD_BUTTON_TEXT = "+ 추가"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    # ============================================================
    # PROPERTIES
    # ============================================================ 
    @property
    def name_input(self):
        """Security Group 생성 모달 - 이름 입력 필드 locator"""
        return self.page.locator(self.NAME_INPUT)

    @property
    def desc_input(self):
        """Security Group 생성 모달 - 설명 입력 필드 locator"""
        return self.page.locator(self.DESC_INPUT)
    
    @property
    def edit_confirm_button(self):
        """모달 - 수정 버튼"""
        dialog = self._get_dialog()
        return dialog.locator('button[aria-label="수정"]').first
    
    # ======== Inbound 규칙 생성 ========
    @property
    def ip_input(self):
        """CIDR - IP 입력 필드"""
        return self.page.locator("#remote-ip")
    
    @property
    def port_min_input(self):
        """단일 포트 - 포트 / 범위 포트 - 시작 값 입력 필드"""
        return self.page.locator("#port-min")
    
    @property
    def port_max_input(self):
        """범위 포트 - 시작 값 입력 필드"""
        return self.page.locator("#port-max")
    
    @property
    def select_box(self):
        """셀렉트 박스 locator"""
        return self.page.get_by_role("combobox")
    
    @property
    def remote_group(self):
        """보안 그룹 선택 박스 locator"""
        return self.page.locator("#remote-group")
    
    # ============================================================
    # ACTIONS
    # ============================================================
    def enter_name(self, name: str):
        """Security Group 이름 입력"""
        self.name_input.fill(name)

    def enter_desc(self, desc: str):
        """Security Group 설명 입력"""
        self.desc_input.fill(desc)

    def fill_form(self, name: str, desc: str):
        """Security Group 폼 입력"""
        self.enter_name(name)
        self.enter_desc(desc)

    # ======== Inbound 규칙 생성 ========
    def enter_ip(self, ip: str):
        """Inbound IP 입력"""
        self.ip_input.fill(ip)

    def enter_min_port(self, port: int):
        """단일 포트 - 포트 / 범위 포트 - 시작 값 입력"""
        self.port_min_input.fill(str(port))

    def enter_max_port(self, port: int):
        """범위 포트 - 끝 값 입력"""
        self.port_max_input.fill(str(port))

    def get_selectbox_by_label(self, label_text: str):
        """
        <label>라벨 텍스트</label> 바로 아래에 있는
        button[role="combobox"][data-slot="select-trigger"]를 찾아서 반환.
        """
        container = self.page.locator("div").filter(
            has=self.page.locator("label", has_text=label_text)
        ).first

        return container.locator('button[role="combobox"][data-slot="select-trigger"]').first

    def open_selectbox_by_label(self, label_text: str, timeout: int = 10000) -> None:
        """라벨 기준으로 셀렉트박스를 열기"""
        print('label_text ::', label_text)
        selectbox = self.get_selectbox_by_label(label_text)
        print('selectbox ::', selectbox)
        selectbox.click()

    def open_selectbox_by_name(self, name: str):
        selectbox = self.select_box.filter(has_text=name).first
        selectbox.click()
    
    def select_option_by_name(self, name: str):
        option = self.page.get_by_role("option", name=name).first
        self._safe_click(option)

    # ===== 테스트 시나리오 단위 ACTIONS =====
    def create_sg(self, sg_name: str, desc: str,) -> str:
        """Security Group 생성 플로우"""
        self.open_create_modal(C.SG_CREATE)
        self.fill_form(name=sg_name, desc=desc)
        self.click_button(text=B.CREATE_BUTTON_NAME)

        return sg_name
    
    def update_sg(self, sg_name: str, new_name: str, desc: str):
        """Security Group 수정 플로우"""
        self.go_link_by_name(name=sg_name)
        self.open_modal(text="수정")
        self.fill_form(name=new_name, desc=desc)
        self._safe_click(self.edit_confirm_button)
    
    def delete_sg(self, sg_name: str):
        """Security Group 삭제 플로우"""
        # self.go_link_by_name(name=sg_name)
        self.open_delete_modal()
        self.run_delete_flow()

    def add_all_protocol(self, ip):
        """All 프로토콜 + CIDR"""
        self.open_selectbox_by_name(self.CUSTOM_TCP)
        self.select_option_by_name(name=self.ALL_PROTOCOL)

        self.enter_ip(ip)

        self.click_button(text=self.ADD_BUTTON_TEXT)

    def add_all_tcp(self):
        """All TCP + 보안그룹"""
        self.open_selectbox_by_name(self.ALL_PROTOCOL)
        self.select_option_by_name(name=self.ALL_TCP)

        self.open_selectbox_by_name(name=self.CIDR)
        self.select_option_by_name(name=self.SECURITY_GROUP)

        self._safe_click(self.remote_group)
        self.select_option_by_name("default")

        self.click_button(text=self.ADD_BUTTON_TEXT)

    def add_custom_tcp(self, port, ip):
        """사용자정의 TCP + 단일포트 + CIDR"""
        self.open_selectbox_by_name(self.ALL_TCP)
        self.select_option_by_name(name=self.CUSTOM_TCP)

        self.enter_min_port(port)

        self.open_selectbox_by_name(name=self.SECURITY_GROUP)
        self.select_option_by_name(name=self.CIDR)

        self.enter_ip(ip)

        self.click_button(text=self.ADD_BUTTON_TEXT)

    def add_custom_udp(self, min_port, max_port):
        """사용자정의 UDP + 범위포트 + 보안 그룹"""
        self.open_selectbox_by_name(self.CUSTOM_TCP)
        self.select_option_by_name(name=self.CUSTOM_UDP)

        self.open_selectbox_by_name(self.PORT_UNIT)
        self.select_option_by_name(self.PORT_RANGE)
        self.enter_min_port(min_port)
        self.enter_max_port(max_port)

        self.open_selectbox_by_name(name=self.CIDR)
        self.select_option_by_name(name=self.SECURITY_GROUP)

        self._safe_click(self.remote_group)
        self.select_option_by_name("default")

        self.click_button(text=self.ADD_BUTTON_TEXT)

    def create_inbound_rules(self, ip: str, port: int):
        """
        Security Group Inbound 생성 플로우
        
        All 프로토콜 + CIDR
        All TCP + 보안 그룹
        Custom TCP + 단일포트 + CIDR
        Custom UDP + 범위포트 + 보안 그룹
        """

        # self.go_link_by_name(name=sg_name)
        self.open_create_modal(C.INBOUND_CREATE)

        self.add_all_protocol(ip)
        self.add_all_tcp()
        self.add_custom_tcp(port, ip)
        self.add_custom_udp(min_port = 10, max_port = 100)

        self.click_button(text=B.CREATE_TEXT)
    