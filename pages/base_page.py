from datetime import datetime
from pathlib import Path
from playwright.sync_api import Page, expect

class BasePage:
    SCREENSHOT_DIR = Path("artifacts/screenshots")

    def __init__(self, page: Page):
        self.page = page

    # ===== 공통 네비게이션 / 로딩 =====
    def open(self, url: str):
        """특정 URL로 이동"""
        self.page.goto(url)

    def click_button(self, text: str, timeout: int = 10000):
        """텍스트 기반 버튼 클릭 (보일 때까지 기다렸다가 클릭)"""
        btn = self.button_by_text(text)
        expect(btn).to_be_visible(timeout=timeout)
        btn.click()

    # ===== 토스트/알림 공통 처리 =====
    def wait_for_toast(self, text: str, timeout: int = 5000):
        """성공/오류 토스트 등 공통 알림 텍스트 대기"""
        toast = self.page.get_by_text(text)
        expect(toast).to_be_visible(timeout=timeout)
        return toast

    # ===== 스크린샷 유틸 =====
    def take_screenshot(self, name: str = "screenshot") -> str:
        """
        실패 디버깅용 스크린샷 저장
        반환값: 저장된 파일 경로(str)
        """
        self.SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        file_path = self.SCREENSHOT_DIR / f"{name}_{ts}.png"
        self.page.screenshot(path=str(file_path), full_page=True)
        return str(file_path)

    # ===== 공통 assert =====
    def assert_text_visible(self, text: str, timeout: int = 5000):
        expect(self.page.get_by_text(text)).to_be_visible(timeout=timeout)
