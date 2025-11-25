import time
from playwright.sync_api import Page, expect
from pages.locators.common import ToastLocators as T, ButtonLocators as B
from pages.locators.actions import SidebarLocators as S

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # ============================================================
    # PROPERTIES
    # ============================================================ 
    @property
    def name_cell(self):
        """이름 셀"""
        return self.page.locator(".ag-pinned-left-cols-container [role='gridcell'][col-id='name']")
    
    @property
    def delete_open_button(self):
        """삭제 버튼"""
        return self.page.locator("button.s-button--danger", has_text=B.DELETE_TEXT)

    @property
    def delete_input(self):
        """모달 - 삭제 입력 필드"""
        return self.page.get_by_role("textbox", name="input")

    @property
    def delete_confirm_button(self):
        """모달 - 삭제 버튼"""
        return self.page.locator('button[aria-label="삭제"]')
    
    @property
    def edit_name_input(self):
        """이름 필드"""
        return self.page.locator('input[aria-label="input"]')
    
    @property
    def pen_button(self):
        """이름 수정시 펜 버튼"""
        return self.page.locator("button.s-icon-button--small").filter(has=self.page.locator('span[aria-label="pen"]')).first
    
    @property
    def check_button(self):
        """이름 수정 시 체크 버튼"""
        return self.page.locator("button.s-icon-button--small").filter(
            has=self.page.locator('span[aria-label="check"]')
        ).first

    # ============================================================
    # ACTIONS
    # ============================================================
    def go_manage_admin(self, timeout: int = 10000):
        """관리자 메뉴로 이동"""
        admin_button = self.page.get_by_role("button", name=S.ADMIN_MENU, exact=True)
        expect(admin_button).to_be_visible(timeout=timeout)
        admin_button.click()

    def go_console_menu(self, label: str, timeout: int = 10000):
        """사이드바 메뉴 이동(콘솔)"""
        menu_item = self.page.get_by_role("button", name=label, exact=True)
        expect(menu_item).to_be_visible(timeout=timeout)
        menu_item.click()

    def go_admin_menu(self, label: str, timeout: int = 10000):
        """사이드바 메뉴 이동(관리자)"""
        menu_item = self.page.get_by_role("listitem").filter(has_text=label)
        expect(menu_item).to_be_visible(timeout=timeout)
        menu_item.click()
    
    def open_create_modal(self, text: str, timeout: int = 10000):
        """생성 모달 오픈"""
        create_btn = (self.page.locator("button").filter(has_text=text).first)
        expect(create_btn).to_be_visible(timeout=timeout)
        create_btn.click()

    def click_button(self, text: str = B.CONFIRM_TEXT, timeout: int = 20000):
        """버튼 locator 클릭"""
        btn = self.page.get_by_role("button", name=text).first
        try:
            expect(btn).to_be_visible(timeout=timeout)
            expect(btn).to_be_enabled(timeout=timeout)
            btn.click()
        except Exception:
            # viewport 밖이거나 visibility 체크에서 실패한 경우 강제 클릭
            expect(btn).to_be_attached(timeout=timeout)
            btn.evaluate("el => el.click()")

    def open_project(self, project_name: str = "QA-PROJECT-001", timeout: int = 10000):
        """프로젝트 리스트에서 특정 프로젝트 클릭하여 진입"""
        link = self.page.get_by_role("link", name=project_name)
        expect(link).to_be_visible(timeout=timeout)
        link.click()

    def go_link_by_name(self, name: str, timeout: int = 10000) -> None:
        """이름 링크 페이지로 이동"""
        cell = self.name_cell.filter(has_text=name).first
        expect(cell).to_be_visible(timeout=timeout)

        link = cell.locator("a").first
        expect(link).to_be_visible(timeout=timeout)

        link.click()

    def run_rename_flow(self, new_name: str, timeout: int = 10000) -> str:
        """이름 수정(펜) 클릭 > 수정 > 저장"""
        pen_btn = self.pen_button
        expect(pen_btn).to_be_enabled(timeout=timeout)
        pen_btn.click()

        self.edit_name_input.fill(new_name)

        check_btn = self.check_button
        expect(check_btn).to_be_enabled(timeout=timeout)
        check_btn.click()
        
    def open_delete_modal(self, timeout: int = 10000):
        """삭제 모달 오픈"""
        open_btn = self.delete_open_button
        expect(open_btn).to_be_visible(timeout=timeout)
        open_btn.click()
        
    def run_delete_flow(self, timeout: int = 10000) -> None:
        """삭제 텍스트 입력 > 최종 삭제 버튼 클릭"""
        input = self.delete_input
        expect(input).to_be_visible(timeout=timeout)
        input.fill(B.DELETE_TEXT)

        confirm_btn = self.delete_confirm_button
        expect(confirm_btn).to_be_enabled(timeout=timeout)
        confirm_btn.click()

    def open_modal(self, text: str, timeout: int = 10000):
        """모달 오픈"""
        # s-button s-button--medium s-button--secondary
        btn = self.page.locator("button.s-button--secondary", has_text=text)
        expect(btn).to_be_visible(timeout=timeout)
        btn.click()

    def run_modal_flow(self, text: str, timeout: int = 10000):
        """텍스트 입력 > 최종 삭제 버튼 클릭"""
        input = self.page.get_by_role("textbox", name="input")
        expect(input).to_be_visible(timeout=timeout)
        input.fill(text)

        confirm_btn = self.page.locator(f'button[aria-label="{text}"]')
        expect(confirm_btn).to_be_enabled(timeout=timeout)
        confirm_btn.click()

    # NOTE: 20251125 아직 수정중인 코드
    def wait_toast_success_or_fail(
        self,
        success_text: str,
        fail_text: str,
        timeout: int = 5000,
        poll_interval: float = 0.2,
    ) -> None:
        """현재 페이지에 떠 있는 모든 alert 토스트를 스캔하며 즉시 성공 또는 실패로 판정"""

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
    