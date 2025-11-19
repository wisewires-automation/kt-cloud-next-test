import os, inspect, zipfile
from datetime import datetime
from pathlib import Path
from playwright.sync_api import Page
from dotenv import load_dotenv

load_dotenv()

class ScreenshotSession:
    
    def __init__(self, base_file: str | Path | None = None, zip_name: str | None = None, is_root: bool = False):

        if base_file is None:
            caller_frame = inspect.stack()[1]
            base_file = caller_frame.filename

        base_path = Path(base_file).resolve()
        self.base_path = base_path

        # 스크린샷 루트 경로 결정
        sc_path = os.getenv("SCREENSHOT_PATH")

        if is_root:
            # 기본값: "최상위 폴더 밑에 screenshots"
            project_root = base_path.parents[1]
        else:
            project_root = Path(sc_path).expanduser()

        self.screenshot_dir = project_root / "screenshots"
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)

        print(f"zip 저장 경로: {self.screenshot_dir}, zip 파일명: {zip_name}")

        if zip_name is None:
            zip_name = base_path.stem
        self.zip_file = self.screenshot_dir / f"{zip_name}.zip"

        self._zip = zipfile.ZipFile(self.zip_file, "w", zipfile.ZIP_DEFLATED)

    def snap(self, page: Page, label: str = "", save_img: bool = False):
        safe_label = label.strip().replace(" ", "_").lower() if label else "snap"

        rand = _time_suffix()
        filename = f"{safe_label}_{rand}.png"

        if save_img:
            filepath = self.screenshot_dir / filename
            page.screenshot(path=str(filepath))
            self._zip.write(filepath, arcname=filename)
        else:
            png_bytes = page.screenshot()
            self._zip.writestr(filename, png_bytes)
        
        print(f"[ScreenshotSession] zip에 이미지 추가: {filename}")

    def close(self):
        if self._zip:
            self._zip.close()
            self._zip = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()


def quick_snap(page: Page, label: str = "", base_file: str | Path | None = None) -> Path:
    """
    zip 없이 한 장만 캡쳐
    """
    if base_file is None:
        base_file = inspect.stack()[1].filename

    base_path = Path(base_file).resolve()
    ss_dir = base_path.parent / "screenshots"
    ss_dir.mkdir(exist_ok=True)

    safe_label = label.strip().replace(" ", "_").lower() if label else "snap"
    rand = _time_suffix()

    filename = f"{safe_label}_{rand}.png"
    filepath = ss_dir / filename

    page.screenshot(path=str(filepath))
    print(f"[quick_snap] 캡쳐 저장: {filepath}")

    return filepath

def _time_suffix() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")