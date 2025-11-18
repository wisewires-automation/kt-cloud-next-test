import time
import zipfile
from pathlib import Path

class screenshots:
    def __init__(self, screenshot_dir: Path, zip_file: Path):
        self.screenshot_dir = screenshot_dir
        self.zip_file = zip_file
        self.step = 1
        self.zip = zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED)
    
    def snap(self, page, label: str = ""):
        filename = f"step{self.step:02d}_{label}.png"
        filepath = self.screenshot_dir / filename

        page.screenshot(path=str(filepath))

        self.zip.write(filepath, arcname=filename)
        print(f"zip 파일에 이미지 넣기: {filename}")
        self.step += 1

    def zip_close(self):
        self.zip.close()
