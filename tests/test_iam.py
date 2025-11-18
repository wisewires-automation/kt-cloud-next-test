from pages.user_page import UserPage
from pages.role_page import RolePage
import time

def test_create_iam_user(kt_logged_in_page, iam_user_info, log):
    """
    ADMIN 계정에서 IAM 사용자 계정 생성
    """
    page = kt_logged_in_page
    
    id              = iam_user_info["id"]
    name            = iam_user_info["name"]
    email           = iam_user_info["email"]
    phone           = iam_user_info["phone"]
    password        = iam_user_info["password"]

    user_page = UserPage(page)

    log.info("[ADMIN] 관리자 페이지 이동")
    user_page.go_manage_admin()

    log.info("[ADMIN] IAM 사용자 생성 시작")
    user_page.create_user(id=id,name=name,email=email,phone=phone,password=password)

    log.info("[ADMIN] IAM 사용자 생성 완료 | id=%s", id)

def test_grant_role(kt_logged_in_page, iam_user_info, log):
    """
    ADMIN 계정에서 IAM 사용자 권한 부여
    """
    page = kt_logged_in_page

    user_page = UserPage(page)
    role_page = RolePage(page)

    id = iam_user_info["id"]

    log.info("[ADMIN] 관리자 페이지 이동")
    user_page.go_manage_admin()

    log.info("[ADMIN] IAM 사용자 클릭 | id=%s", id)
    role_page.click_user_row(id=id)
    role_page.click_role_edit()

    # log.info("[ADMIN] 라디오 그룹 선택")
    # role_page.click_radio_group(is_org=False)

    log.info("[ADMIN] 역할 선택")
    role_page.click_role_checkbox_by_name("USER_MANAGER")

    time.sleep(5)


def test_login_iam_user(iam_logged_in_page, iam_user_info, log):
    """새 페이지에서 방금 생성한 IAM 계정으로 로그인 검증"""
    page = iam_logged_in_page

    log.info("[test_login_iam_user] IAM 로그인 확인 | id=%s, email=%s",
             iam_user_info["id"], iam_user_info["email"])
