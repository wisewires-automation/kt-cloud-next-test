from playwright.sync_api import Page, expect
from utils.namer import make_name

class ServerPage:

    # ===== selector / text 상수 =====
    SERVER_NAV_BUTTON_NAME = "Server"
    SERVER_CREATE_BUTTON_NAME = "Server 생성"

    # 이미지 / 스펙 라디오
    SERVER_IMAGE_RADIO_NAME = "windows-2019-mssql-2017-std-"
    SERVER_SPEC_RADIO_NAME = "32x32-amd 32 32 미정 미정"

    # AZ / 서버명
    DEFAULT_AZ_NAME = "DX-G-GB-A"
    SERVER_NAME_TEXTBOX_ROLE_NAME = "input"

    # Volume
    VOLUME_CREATE_BUTTON_TEXT = "Volume 생성"

    # Subnet
    SUBNET_CREATE_BUTTON_TEXT = "Subnet 생성"

    # NIC
    NIC_CREATE_BUTTON_TEXT = "신규 NIC 생성"
    NIC_PUBLIC_IP_CHECKBOX_SELECTOR = (
        ".s-checkbox.s-checkbox--medium.s-checkbox--default.s-checkbox--hover "
        "> .s-checkbox__input-wrapper > .s-checkbox__checkmark"
    )

    # KeyPair
    KEYPAIR_DIALOG_NAME = "Key Pair 생성"
    KEYPAIR_INPUT_LABEL = "input"
    KEYPAIR_CREATE_BUTTON_NAME = "생성"
    KEYPAIR_SELECT_COMBO_NAME = "선택하세요"

    CONFIRM_BUTTON_NAME = "서버 생성"

    def __init__(self, page: Page):
        self.page = page

        self.server_nav_button = page.get_by_role("button", name=self.SERVER_NAV_BUTTON_NAME, exact=True)
        self.server_create_button = (page.locator("button").filter(has_text=self.SERVER_CREATE_BUTTON_NAME).first)

        self.confirm_button = page.get_by_role("button",name=self.CONFIRM_BUTTON_NAME)

    # ===== 공통 동작 =====
    def go_server_create(self, timeout: int = 10000):
        """Server 메뉴 이동 후 'Server 생성' 페이지 진입"""
        expect(self.server_nav_button).to_be_visible(timeout=timeout)
        self.server_nav_button.click()

        expect(self.server_create_button).to_be_visible(timeout=timeout)
        self.server_create_button.click()

     # ===== 3) 서버 이미지 선택 =====
    def select_server_image(self, image_name: str | None = None, timeout: int = 10000):
        if image_name is None:
            image_name = self.SERVER_IMAGE_RADIO_NAME

        image_radio = self.page.get_by_role("radio", name=image_name)
        expect(image_radio).to_be_visible(timeout=timeout)
        image_radio.click()

    # ===== 4) 서버 스펙 선택 =====
    def select_server_spec(self, spec_name: str | None = None, timeout: int = 10000):
        if spec_name is None:
            spec_name = self.SERVER_SPEC_RADIO_NAME

        spec_radio = self.page.get_by_role("radio", name=spec_name)
        expect(spec_radio).to_be_visible(timeout=timeout)
        spec_radio.click()

    # ===== 5) 서버 기본정보 (AZ + 서버 이름) =====
    def fill_basic_info(
        self,
        az_name: str | None = None,
        server_name: str = "server-name-01",
        timeout: int = 10000,
    ):
        """
        5-1) Availability Zone 선택
        5-2) 서버 이름 입력
        """
        if az_name is None:
            az_name = self.DEFAULT_AZ_NAME

        # AZ 콤보박스
        az_combobox = self.page.get_by_role("combobox")
        expect(az_combobox).to_be_visible(timeout=timeout)
        az_combobox.click()

        az_option = self.page.get_by_role("option", name=az_name)
        expect(az_option).to_be_visible(timeout=timeout)
        az_option.click()

        # 서버 이름 textbox (role="textbox", name="input")
        name_textbox = self.page.get_by_role(
            "textbox",
            name=self.SERVER_NAME_TEXTBOX_ROLE_NAME,
        )
        expect(name_textbox).to_be_visible(timeout=timeout)
        name_textbox.fill(server_name)

    # ===== 6) Volume 생성 =====
    def create_volume(
        self,
        volume_name: str = "vo-01",
        description: str = "vo-01 desc",
        size: str = "128",
        az_name: str | None = None,
        timeout: int = 10000,
    ):
        """
        6) Volume 생성 플로우
        """
        if az_name is None:
            az_name = self.DEFAULT_AZ_NAME

        # Volume 생성 버튼 클릭
        volume_create_button = (
            self.page.locator("button")
            .filter(has_text=self.VOLUME_CREATE_BUTTON_TEXT)
            .first
        )
        expect(volume_create_button).to_be_visible(timeout=timeout)
        volume_create_button.click()

        # Dialog 안의 입력
        name_input = self.page.locator(self.VOLUME_NAME_INPUT)
        desc_input = self.page.locator(self.VOLUME_DESC_INPUT)

        expect(name_input).to_be_visible(timeout=timeout)
        name_input.fill(volume_name)

        expect(desc_input).to_be_visible(timeout=timeout)
        desc_input.fill(description)

        # Volume 타입 선택 (Data Volume : be 1 (block...))
        vol_type_combo = self.page.get_by_role("combobox", name=self.VOLUME_TYPE_SELECT_NAME)
        expect(vol_type_combo).to_be_visible(timeout=timeout)
        vol_type_combo.click()

        vol_type_option = self.page.get_by_text(self.VOLUME_TYPE_TEXT)
        expect(vol_type_option).to_be_visible(timeout=timeout)
        vol_type_option.click()

        # 크기 입력 (dialog 기준)
        volume_dialog = self.page.get_by_role("dialog", name=self.VOLUME_DIALOG_NAME)
        size_input = volume_dialog.locator(self.VOLUME_SIZE_INPUT)
        expect(size_input).to_be_visible(timeout=timeout)
        size_input.fill(size)

        # AZ 선택 (다시 combobox "선택하세요")
        az_combo2 = self.page.get_by_role("combobox", name=self.VOLUME_TYPE_SELECT_NAME)
        expect(az_combo2).to_be_visible(timeout=timeout)
        az_combo2.click()

        az_option2 = (
            self.page.get_by_test_id(self.VOLUME_ZONE_OPTION_LIST_TESTID)
            .get_by_text(az_name)
        )
        expect(az_option2).to_be_visible(timeout=timeout)
        az_option2.click()

        # 확인 버튼 클릭
        confirm_button = self.page.get_by_role(
            "button",
            name=self.VOLUME_CREATE_CONFIRM_BUTTON_NAME,
        )
        expect(confirm_button).to_be_visible(timeout=timeout)
        confirm_button.click()

        # Volume 생성 성공 토스트
        expect(
            self.page.get_by_text(self.VOLUME_CREATE_SUCCESS_TEXT)
        ).to_be_visible(timeout=timeout)

    # ===== 7) Volume 선택 =====
    def select_volume(self, volume_name: str = "vo-01", timeout: int = 10000):
        """
        볼륨 리스트에서 volume_name 이 포함된 행의 체크박스 선택
        """
        # row 역할을 가정하고, 해당 텍스트 포함된 행에서 체크박스 선택
        row = self.page.get_by_role("row").filter(has_text=volume_name)
        checkbox = row.get_by_role("checkbox")
        expect(checkbox).to_be_visible(timeout=timeout)
        checkbox.click()
    
    # ===== 8) VPC 선택 (UI에 맞게 수정 가능) =====
    def select_vpc(self, vpc_name: str, timeout: int = 10000):
        """
        8) VPC 선택
        (vpc 선택을 위한 combobox/option 구조는 실제 UI에 맞게 필요 시 수정)
        예: combobox 'vpc 선택' → vpc_name 클릭
        """
        vpc_combobox = self.page.get_by_role("combobox", name="vpc 선택")
        expect(vpc_combobox).to_be_visible(timeout=timeout)
        vpc_combobox.click()

        option = self.page.get_by_text(vpc_name)
        expect(option).to_be_visible(timeout=timeout)
        option.click()

    # ===== 9) Subnet 생성 및 선택 =====
    def create_subnet(
        self,
        subnet_name: str = "sub-name-01",
        cidr: str = "10.0.0.0/8",
        timeout: int = 10000,
    ):
        subnet_create_button = (
            self.page.locator("button")
            .filter(has_text=self.SUBNET_CREATE_BUTTON_TEXT)
            .first
        )
        expect(subnet_create_button).to_be_visible(timeout=timeout)
        subnet_create_button.click()

        # 이름 입력
        name_input = self.page.get_by_placeholder(self.SUBNET_NAME_PLACEHOLDER)
        expect(name_input).to_be_visible(timeout=timeout)
        name_input.click()
        name_input.fill(subnet_name)

        # CIDR 입력
        cidr_input = self.page.get_by_placeholder(self.SUBNET_CIDR_PLACEHOLDER)
        expect(cidr_input).to_be_visible(timeout=timeout)
        cidr_input.click()
        cidr_input.fill(cidr)

        # 확인 클릭
        confirm_button = self.page.get_by_role(
            "button",
            name=self.SUBNET_CREATE_CONFIRM_BUTTON_NAME,
        )
        expect(confirm_button).to_be_visible(timeout=timeout)
        confirm_button.click()

        # Subnet 생성 성공 토스트
        expect(
            self.page.get_by_text(self.SUBNET_CREATE_SUCCESS_TEXT)
        ).to_be_visible(timeout=timeout)

    def select_subnet(
        self,
        subnet_name: str = "sub-name-01",
        cidr: str = "10.0.0.0/8",
        timeout: int = 10000,
    ):
        """
        subnet 선택 콤보박스에서 'subnet_name (cidr)' 선택
        """
        subnet_combo = (
            self.page.get_by_role("combobox")
            .filter(has_text=self.SUBNET_SELECT_FILTER_TEXT)
            .first
        )
        expect(subnet_combo).to_be_visible(timeout=timeout)
        subnet_combo.click()

        display_text = f"{subnet_name} ({cidr})"
        option = self.page.get_by_text(display_text)
        expect(option).to_be_visible(timeout=timeout)
        option.click()

    # ===== 9) NIC 생성 및 선택 =====
    def create_nic(
        self,
        nic_name: str = "net-inter-01",
        assign_public_ip: bool = True,
        timeout: int = 10000,
    ):
        """
        신규 NIC 생성 플로우
        """
        nic_create_button = (
            self.page.locator("button")
            .filter(has_text=self.NIC_CREATE_BUTTON_TEXT)
            .first
        )
        expect(nic_create_button).to_be_visible(timeout=timeout)
        nic_create_button.click()

        name_input = self.page.locator(self.NIC_NAME_INPUT)
        expect(name_input).to_be_visible(timeout=timeout)
        name_input.fill(nic_name)

        if assign_public_ip:
            checkbox = self.page.locator(self.NIC_PUBLIC_IP_CHECKBOX_SELECTOR)
            expect(checkbox).to_be_visible(timeout=timeout)
            checkbox.click()

        dialog = self.page.get_by_role("dialog", name=self.NIC_DIALOG_NAME)
        confirm_button = dialog.get_by_role(
            "button",
            name=self.NIC_CREATE_CONFIRM_BUTTON_NAME,
        )
        expect(confirm_button).to_be_visible(timeout=timeout)
        confirm_button.click()

    def select_nic_radio_by_index(page: Page, index: int, timeout: int = 10_000):
        # radiogroup 컨테이너 잡기 (여러 개면 .nth(0) 처럼 더 좁혀도 됨)
        group = page.get_by_role("radiogroup").first

        # radiogroup 안의 radio들 중 index번째 (0부터 시작)
        radio = group.get_by_role("radio").nth(index)

        expect(radio).to_be_visible(timeout=timeout)
        radio.click()

    # ===== 10) KeyPair 생성 및 선택 =====
    def create_and_select_keypair(
        self,
        key_name: str = "key-a",
        timeout: int = 10000,
    ):
        """
        Key Pair 생성 후 드롭다운에서 선택
        """
        dialog = self.page.get_by_role("dialog", name=self.KEYPAIR_DIALOG_NAME)

        key_input = dialog.get_by_label(self.KEYPAIR_INPUT_LABEL)
        expect(key_input).to_be_visible(timeout=timeout)
        key_input.fill(key_name)

        create_button = self.page.get_by_role(
            "button",
            name=self.KEYPAIR_CREATE_BUTTON_NAME,
            exact=True,
        )
        expect(create_button).to_be_visible(timeout=timeout)
        create_button.click()

        # 생성 후 KeyPair 선택
        combo = self.page.get_by_role("combobox", name=self.KEYPAIR_SELECT_COMBO_NAME)
        expect(combo).to_be_visible(timeout=timeout)
        combo.click()

        option = self.page.get_by_text(key_name)
        expect(option).to_be_visible(timeout=timeout)
        option.click()

    # ===== 11) 서버 생성 버튼 클릭 =====
    def submit(self, timeout: int = 20000):
        """
        서버 생성 버튼 클릭
        (서버 생성 성공 토스트가 따로 있다면 여기서 추가 검증 가능)
        """
        expect(self.confirm_button).to_be_visible(timeout=timeout)
        self.confirm_button.click()

    def submit(self, timeout: int = 20000):
        expect(self.confirm_button).to_be_visible(timeout=timeout)
        self.confirm_button.click()

    def create_server(
        self,
        server_name: str = "server-name-01",
        vpc_name: str | None = None,
        volume_name: str = "vo-01",
        subnet_name: str = "sub-name-01",
        subnet_cidr: str = "10.0.0.0/8",
        nic_name: str = "net-inter-01",
        keypair_name: str = "key-a",
        timeout: int = 20000,
    ):
        """
        1) 서버 페이지 진입
        2) 이미지 선택
        3) 스펙 선택
        4) AZ + 서버 이름 입력
        5) Volume 생성 및 선택
        6) VPC 선택 (vpc_name 인자 필요)
        7) Subnet 생성 및 선택
        8) NIC 생성
        9) KeyPair 생성 및 선택
        10) 서버 생성 버튼 클릭
        """
        self.go_server_create(timeout=timeout)
        self.select_server_image(timeout=timeout)
        self.select_server_spec(timeout=timeout)
        self.fill_basic_info(server_name=server_name, timeout=timeout)

        self.create_volume(
            volume_name=volume_name,
            description=f"{volume_name} desc",
            timeout=timeout,
        )
        self.select_volume(volume_name=volume_name, timeout=timeout)

        if vpc_name:
            self.select_vpc(vpc_name=vpc_name, timeout=timeout)

        self.create_subnet(
            subnet_name=subnet_name,
            cidr=subnet_cidr,
            timeout=timeout,
        )
        self.select_subnet(
            subnet_name=subnet_name,
            cidr=subnet_cidr,
            timeout=timeout,
        )

        self.create_nic(
            nic_name=nic_name,
            assign_public_ip=True,
            timeout=timeout,
        )

        self.create_and_select_keypair(
            key_name=keypair_name,
            timeout=timeout,
        )

        self.submit(timeout=timeout)

