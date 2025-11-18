from pathlib import Path
from playwright.sync_api import Page
from pages.user_page import UserPage

from utils.capture import screenshots 

def create_iam_user_scenario(page: Page, iam_user_info: dict, log) -> str:
    """
    ADMIN 계정에서 IAM 사용자 1명 생성 시나리오
    """

    user_id   = iam_user_info["id"]
    name      = iam_user_info["name"]
    email     = iam_user_info["email"]
    phone     = iam_user_info["phone"]
    password  = iam_user_info["password"]

    user_page = UserPage(page)

    log.info("[ADMIN] 관리자 페이지 이동")
    user_page.go_manage_admin()

    log.info("[ADMIN] IAM 사용자 생성 시작")
    log.info("        - id=%s, name=%s, email=%s, phone=%s", user_id, name, email, phone)

    user_page.create_user(
        id=user_id,
        name=name,
        email=email,
        phone=phone,
        password=password,
    )

    log.info("[ADMIN] IAM 사용자 생성 완료 | id=%s", user_id)

        # ===== 여기서 '마지막 화면' 한 장만 캡처 + zip =====
    base_dir = Path(__file__).resolve().parent      # scenarios/ 디렉터리
    ss_dir = base_dir.parent / "screenshots"        # 프로젝트 루트/screenshots
    ss_dir.mkdir(exist_ok=True)

    zip_file = ss_dir / f"{Path(__file__).stem}.zip"

    sc = screenshots(ss_dir, zip_file)
    # label은 서버 이름 정도만 넣어두면 나중에 구분하기 편함
    sc.snap(page, label=f"{user_id}")
    sc.zip_close()

    return user_id
