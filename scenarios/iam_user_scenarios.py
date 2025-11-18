from playwright.sync_api import Page
from pages.user_page import UserPage


def create_iam_user_scenario(page: Page, iam_user_info: dict, log) -> str:
    """
    ADMIN 계정에서 IAM 사용자 1명 생성 시나리오

    전제조건
    - page: 이미 ADMIN(KT) 계정으로 로그인된 상태
    - iam_user_info: id / name / email / phone / password 를 포함한 dict

    반환값
    - 생성한 IAM 사용자 id
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

    return user_id
