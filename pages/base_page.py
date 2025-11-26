import time
from playwright.sync_api import Page, expect
from pages.locators.common import ToastLocators as T, ButtonLocators as B
from pages.locators.actions import SidebarLocators as S

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # ============================================================
    # INTERNAL GENERIC HELPERS (공용 헬퍼)
    # ============================================================
    def _wait_visible(self, locator, timeout: int = 10000):
        """locator가 visible 될 때까지 기다린 후 locator 반환"""
        expect(locator).to_be_visible(timeout=timeout)
        return locator

    def _wait_enabled(self, locator, timeout: int = 10000):
        """locator가 enabled 될 때까지 기다린 후 locator 반환"""
        expect(locator).to_be_enabled(timeout=timeout)
        return locator

    def _safe_click(self, locator, timeout: int = 10000):
        """기본 클릭 + 실패 시 attach만 확인하고 JS로 강제 클릭."""
        try:
            self._wait_visible(locator, timeout)
            self._wait_enabled(locator, timeout)
            locator.click()
        except Exception:
            # viewport 밖이거나 visibility 체크 실패 시 fallback
            expect(locator).to_be_attached(timeout=timeout)
            locator.evaluate("el => el.click()")

    def _get_dialog(self):
        """현재 떠 있는 모달(dialog) 중 마지막 것을 반환 (가장 최근 모달 가정)"""
        return self.page.get_by_role("dialog").last
    
    def _click_button_by_text(self, text: str, timeout: int = 10000, exact: bool = True):
        """role=button + name=text 버튼 공통 클릭"""
        btn = self.page.get_by_role("button", name=text, exact=exact).first
        self._safe_click(btn, timeout=timeout)

    # ============================================================
    # PROPERTIES
    # ============================================================
    @property
    def name_cell(self):
        """이름 셀"""
        return self.page.locator(".ag-pinned-left-cols-container [role='gridcell'][col-id='name']")

    @property
    def delete_open_button(self):
        """삭제 버튼 (리스트에서 삭제 모달 여는 버튼)"""
        return self.page.locator("button.s-button--danger", has_text=B.DELETE_TEXT)

    @property
    def delete_input(self):
        """모달 - 삭제 입력 필드"""
        dialog = self._get_dialog()
        return dialog.get_by_role("textbox", name="input")

    @property
    def delete_confirm_button(self):
        """모달 - 삭제 버튼"""
        dialog = self._get_dialog()
        return dialog.locator('button[aria-label="삭제"]').first

    @property
    def edit_name_input(self):
        """이름 필드"""
        return self.page.locator('input[aria-label="input"]')

    @property
    def pen_button(self):
        """이름 수정시 펜 버튼"""
        return (
            self.page.locator("button.s-icon-button--small")
            .filter(has=self.page.locator('span[aria-label="pen"]'))
            .first
        )

    @property
    def check_button(self):
        """이름 수정 시 체크 버튼"""
        return (
            self.page.locator("button.s-icon-button--small")
            .filter(has=self.page.locator('span[aria-label="check"]'))
            .first
        )

    # ============================================================
    # ACTIONS (외부에서 주로 쓰는 메서드)
    # ============================================================
    def click_button(self, text: str = B.CONFIRM_TEXT):
        """텍스트로 버튼 클릭"""
        self._click_button_by_text(text=text)

    def go_manage_admin(self):
        """관리자 메뉴로 이동"""
        admin_button = self.page.get_by_role("button", name=S.ADMIN_MENU, exact=True)
        self._safe_click(admin_button)

    def go_console_menu(self, label: str):
        """사이드바 메뉴 이동(콘솔)"""
        menu_item = self.page.get_by_role("button", name=label, exact=True)
        self._safe_click(menu_item)

    def go_admin_menu(self, label: str):
        """사이드바 메뉴 이동(관리자)"""
        menu_item = self.page.get_by_role("listitem").filter(has_text=label)
        self._safe_click(menu_item)

    def open_modal(self, text: str, timeout: int = 10000):
        """모달 오픈"""
        btn = self.page.locator("button.s-button--secondary", has_text=text)
        self._safe_click(btn, timeout=timeout)

    def open_create_modal(self, text: str, timeout: int = 10000):
        """생성 모달 오픈"""
        btn = self.page.locator("button").filter(has_text=text).first
        self._safe_click(btn, timeout=timeout)

    def open_delete_modal(self, timeout: int = 10000):
        """삭제 모달 오픈"""
        btn = self.delete_open_button
        self._safe_click(btn, timeout=timeout)

    def open_project(self, project_name: str = "QA-PROJECT-001", timeout: int = 10_000):
        """프로젝트 리스트에서 특정 프로젝트 클릭하여 진입"""
        link = self.page.get_by_role("link", name=project_name)
        self._safe_click(link, timeout=timeout)

    def go_link_by_name(self, name: str, timeout: int = 10000) -> None:
        """이름 링크 페이지로 이동"""
        cell = self.name_cell.filter(has_text=name).first
        self._wait_visible(cell, timeout=timeout)
        link = cell.locator("a").first
        self._safe_click(link, timeout=timeout)

    def click_pen_button(self, timeout: int = 10000):
        """펜 버튼(수정) 클릭"""
        self._safe_click(self.pen_button, timeout=timeout)

    def click_check_button(self, timeout: int = 10000):
        """체크 버튼(저장) 클릭"""
        self._safe_click(self.check_button, timeout=timeout)

    def run_rename_flow(self, new_name: str, timeout: int = 10000):
        """이름 수정(펜) 클릭 > 수정 > 저장"""
        self.click_pen_button(timeout=timeout)
        self._wait_visible(self.edit_name_input, timeout=timeout)
        self.edit_name_input.fill(new_name)
        self.click_check_button(timeout=timeout)

    def enter_delete_text(self, timeout: int = 10000):
        """삭제 텍스트 입력"""
        input_box = self.delete_input
        self._wait_visible(input_box, timeout=timeout)
        input_box.fill(B.DELETE_TEXT)
    
    def click_delete_button(self, timeout: int = 10000):
        """삭제 버튼 클릭"""
        self._safe_click(self.delete_confirm_button, timeout=timeout)

    def run_delete_flow(self, timeout: int = 10000) -> None:
        """삭제 텍스트 입력 > 최종 삭제 버튼 클릭"""
        self.enter_delete_text(timeout=timeout)
        self.click_delete_button(timeout=timeout)

    def run_modal_flow(self, text: str, timeout: int = 10000):
        """텍스트 입력 > 최종 삭제 버튼 클릭"""
        input = self.page.get_by_role("textbox", name="input")
        expect(input).to_be_visible(timeout=timeout)
        input.fill(text)

        btn = self.page.locator(f'button[aria-label="{text}"]')
        self._safe_click(btn)

    # ============================================================
    # TOAST WAIT (공용 로직)
    # NOTE: 아직 수정중인 코드
    # ============================================================
    def wait_toast_success_or_fail(
        self,
        success_text: str,
        fail_text: str,
        timeout: int = 5000,
        poll_interval: float = 0.2,
    ) -> None:
        """
        현재 페이지에 떠 있는 모든 alert 토스트를 스캔하며 즉시 성공 또는 실패로 판정
        - success_text / fail_text: 부분 문자열 매칭
        - 둘 중 하나라도 발견되면 즉시 반환(or 예외)
        """

        deadline = time.time() + (timeout / 1000.0)

        while time.time() < deadline:
            alerts = self.page.get_by_role("alert")
            count = alerts.count()

            if count == 0:
                time.sleep(poll_interval)
                continue

            found_success = None  # (title, desc) 저장용
            found_fail = None     # (title, desc) 저장용

            for i in range(count):
                alert = alerts.nth(i)

                title_loc = alert.locator(".s-toast__item__body__title")
                desc_loc = alert.locator(".s-toast__item__body__description")

                # title 이 없는 경우는 토스트가 아닐 수 있으므로 스킵
                try:
                    title_text = title_loc.inner_text().strip()
                except Exception:
                    continue

                try:
                    desc_text = desc_loc.inner_text().strip()
                except Exception:
                    desc_text = ""

                full_text = f"{title_text} {desc_text}"

                # 모든 alert의 메세지 로그
                print(f"[TOAST] alert[{i}] title={title_text!r}, desc={desc_text!r}")

                # 실패 텍스트 포함 여부 확인
                if fail_text and (fail_text in title_text or fail_text in full_text):
                    found_fail = (title_text, desc_text)

                # 성공 텍스트 포함 여부 확인
                if success_text and (success_text in title_text or success_text in full_text):
                    found_success = (title_text, desc_text)

            # 실패 토스트가 하나라도 발견되면 우선 실패 처리
            if found_fail is not None:
                t, d = found_fail
                raise AssertionError("실패 (title={t!r}, desc={d!r})")

            # 성공 토스트가 하나라도 발견되면 성공 처리
            if found_success is not None:
                return

            # 아직 success/fail 텍스트를 가진 토스트가 없다면 재시도
            time.sleep(poll_interval)

        # timeout 동안 성공/실패 텍스트 둘 다 못 찾음
        raise AssertionError("성공/실패 토스트를 찾지 못했습니다.")


        # success_toast = self.page.get_by_text(T.CREATE_SUCCESS_TEXT)
        # fail_toast = self.page.get_by_text(T.CREATE_FAIL_TEXT)
        
        # try:
        #     expect(success_toast).to_be_visible(timeout=timeout)
        # except Exception:
        #     try:
        #         expect(fail_toast).to_be_visible(timeout=timeout)
        #         raise AssertionError("Nework ACL 생성 실패")
        #     except Exception:
        #         raise
    