import time
import os
import inspect
import zipfile
from datetime import datetime
from pathlib import Path
from playwright.sync_api import Page
from dotenv import load_dotenv

load_dotenv()

class ScreenshotSession:
    """
    Playwright Page 스크린샷을 zip 파일 하나에 모아서 저장하는 세션 클래스.

    사용 예시:
        with ScreenshotSession() as sc:
            sc.snap(page, label="login_page")
            sc.snap(page, label="after_submit")
        # with 블록이 끝날 때 zip 자동 close

    - base_file:
        * None인 경우: 이 클래스를 호출한 파일을 기준으로 경로 계산
        * str/Path로 직접 넘기면 그 파일을 기준으로 경로 계산

    - zip_name:
        * None이면 base_file의 파일 이름(stem)을 zip 이름으로 사용
        * 예: test_login.py → test_login.zip

    - is_root:
        * True  이면: base_file 기준으로 "프로젝트 루트" 쪽에 screenshots 디렉토리 생성
        * False 이면: 환경변수 SCREENSHOT_PATH 하위에 screenshots 디렉토리 생성
    """

    def __init__(
        self,
        base_file: str | Path | None = None,
        zip_name: str | None = None,
        is_root: bool = False,
    ):
        # base_file 미지정 시, 이 클래스를 호출한 파일의 경로를 사용
        if base_file is None:
            caller_frame = inspect.stack()[1]
            base_file = caller_frame.filename

        base_path = Path(base_file).resolve()
        self.base_path = base_path

        # 스크린샷 루트 경로 결정
        #   - is_root=True  → base_file 기준 상위 폴더 아래에 screenshots 생성
        #   - is_root=False → 환경변수 SCREENSHOT_PATH 아래에 screenshots 생성
        sc_path = os.getenv("SCREENSHOT_PATH")

        if is_root:
            # 예: /path/to/project/tests/test_login.py
            #     → parents[1] = /path/to/project
            project_root = base_path.parents[1]
        else:
            # 환경변수 SCREENSHOT_PATH가 설정되어 있다고 가정
            # (미설정시 Path(sc_path)에서 에러남)
            project_root = Path(sc_path).expanduser()

        # 실제 스크린샷/zip 파일이 저장될 디렉토리
        self.screenshot_dir = project_root / "screenshots"
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)

        print(f"zip 저장 경로: {self.screenshot_dir}, zip 파일명: {zip_name}")

        # zip 파일명 기본값: base_file.stem.zip
        if zip_name is None:
            zip_name = base_path.stem
        self.zip_file = self.screenshot_dir / f"{zip_name}.zip"

        self._zip = zipfile.ZipFile(self.zip_file, "w", zipfile.ZIP_DEFLATED)

    def snap(self, page: Page, label: str = "", save_img: bool = False):
        """
        현재 페이지 스크린샷을 찍어 zip 파일에 추가.

        - label:
            * 파일명 앞부분에 붙는 라벨
            * 공백은 '_'로 치환, 소문자로 변환
            * 미지정 시 "snap" 사용

        - save_img:
            * False(기본): png 바이트를 직접 zip 안에만 저장 (디스크에 png 파일은 남기지 않음)
            * True       : 먼저 screenshots 디렉토리에 png 파일로 저장 후,
                           그 파일을 zip에 추가
        """
        # 결과 화면 캡쳐를 위해 추가
        time.sleep(1)

        # 파일명용 라벨 정리
        safe_label = label.strip().replace(" ", "_").lower() if label else "snap"

        rand = _time_suffix()
        filename = f"{safe_label}_{rand}.png"

        if save_img:
            # 실제 파일로도 남기는 모드
            filepath = self.screenshot_dir / filename
            page.screenshot(path=str(filepath))
            self._zip.write(filepath, arcname=filename)
        else:
            # 디스크에 파일을 남기지 않고 png bytes를 바로 zip에 기록
            png_bytes = page.screenshot()
            self._zip.writestr(filename, png_bytes)

        print(f"[ScreenshotSession] zip에 이미지 추가: {filename}")

    def close(self):
        """열려있는 zip 핸들을 안전하게 닫는다."""
        if self._zip:
            self._zip.close()
            self._zip = None

    def __enter__(self):
        """with 문 진입 시 세션 객체를 그대로 반환."""
        return self

    def __exit__(self, exc_type, exc, tb):
        """
        with 문 종료 시 자동으로 zip 닫기.
        예외가 발생해도 zip은 닫아준다.
        """
        self.close()


def quick_snap(page: Page, label: str = "", base_file: str | Path | None = None) -> Path:
    """
    zip 없이 스크린샷 한 장만 캡쳐하는 함수

    - base_file:
        * None인 경우: 호출한 파일을 기준으로 같은 폴더 아래 "screenshots" 디렉토리 생성
        * 지정한 경우: 해당 파일 경로 기준으로 "screenshots" 디렉토리 생성

    반환값:
        - 실제로 저장된 png 파일의 전체 경로(Path 객체)
    """
    # base_file 미지정 시, 호출 스택에서 호출자 파일을 가져옴
    if base_file is None:
        base_file = inspect.stack()[1].filename

    base_path = Path(base_file).resolve()
    # 호출한 파일과 같은 폴더에 screenshots 디렉토리 생성
    ss_dir = base_path.parent / "screenshots"
    ss_dir.mkdir(exist_ok=True)

    # 파일명용 라벨 정리
    safe_label = label.strip().replace(" ", "_").lower() if label else "snap"
    rand = _time_suffix()

    filename = f"{safe_label}_{rand}.png"
    filepath = ss_dir / filename

    # 실제 png 파일로 저장
    page.screenshot(path=str(filepath))
    print(f"[quick_snap] 캡쳐 저장: {filepath}")

    return filepath


def _time_suffix() -> str:
    """
    파일명 중복 방지를 위한 시간 생성.
    예: '20251125_093045'
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")