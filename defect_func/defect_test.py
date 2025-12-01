import time
import zipfile
from pathlib import Path
from playwright.sync_api import Playwright, sync_playwright
from datetime import datetime

def IAM_test(p: Playwright):
    browser = None
    context = None
    page = None
    step_counter = 1
    try:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        base_dir = Path(__file__).resolve().parent
        ss_dir = base_dir.parent / "screenshots"
        zip_file = ss_dir / f"{Path(__file__).stem}.zip"

        # 오류 이벤트 등록
        def setup_error_listeners(page):
            page.on("requestfailed", lambda req: print(f"[REQUEST FAILED] {req.url}\n └ 이유: {req.failure}"))
            page.on("response", lambda res: res.status >= 400 and print(f"[BAD RESPONSE] {res.status} {res.url}"))
            page.on("console", lambda msg: msg.type == "error" and print(f"[CONSOLE ERROR] {msg.text}"))
            page.on("pageerror", lambda err: print(f"[PAGE ERROR] {err}"))

        setup_error_listeners(page)

        # 테스트 흐름
        # with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zip_file_obj:

            #kt cloud 페이지 접근
        page.goto("https://console.gcloud.kt.com/auth/signin")
        time.sleep(5)
        page.get_by_role("tab", name = "IAM 계정").click()
        print("IAM 클릭")
        page.get_by_placeholder("조직 아이디 (접속키)").fill("GOV_bychoi_20723")
        print("조직 아이디 클릭")
        page.get_by_placeholder("아이디").fill("QAuser")
        print("아이디 기입")
        page.get_by_placeholder("비밀번호").fill("Wise20030801!")
        time.sleep(2)
        page.get_by_role("button", name="로그인").click()
        print("로그인 시도")
        page.locator('[data-slot="card-title"]', has_text="QA_automation_test").click()
        print("해당 프로젝트 클릭")
        page.locator(".s-vertical-navigation-menu-item__label", has_text="Server").click()
        print("사이드바 - 서버 클릭")
        time.sleep(2)
        page.locator(".s-vertical-navigation-menu-item__label", has_text="Images").click()
        print("사이드바 - 이미지 클릭")
        time.sleep(2)
        page.locator(".s-vertical-navigation-menu-item__label", has_text="NIC (Network Interface)").click()
        print("사이드바 - NIC 클릭")
        time.sleep(2)
        page.locator(".s-vertical-navigation-menu-item__label", has_text="Key Pair").click()
        print("사이드바 - key_pair 클릭")
        time.sleep(2)
        page.get_by_role("button", name="ADMIN").click()
        print("admin 클릭")
        page.locator('span[aria-label="chevron-down"]').click()
        print("드롭다운 버튼 클릭")
        # log_out = page.locator(".s-menu-item__label", has_text="로그아웃")
        # log_out.wait_for()
        # log_out.click()
        # print("로그아웃 클릭")
        page.get_by_role("button", name="확인").click()
        time.sleep(3)
        print("로그인 화면 체크")
    except Exception as ex:
        print(f"IAM 테스트 에러: {ex}")
        try:
            # 에러 스크린샷 파일명 생성
            error_filename = f"{Path(__file__).stem}_error.png"
            # _{datetime.now().strftime('%Y%m%d_%H%M%S')}
            error_filepath = ss_dir / error_filename
            page.screenshot(path=str(error_filepath))
            print(f"예외 스크린샷 저장: {error_filename}")

            # ZIP에 추가
            with zipfile.ZipFile(zip_file, "a", zipfile.ZIP_DEFLATED) as zip_file_obj:
                zip_file_obj.write(error_filepath, arcname=error_filename)
                print(f"예외 스크린샷 ZIP에 추가: {error_filename}")

        except Exception as snap_ex:
            print(f"예외 스크린샷 저장 실패: {snap_ex}")

    finally:
        if context:
            context.close()
        if browser:
            browser.close()
 
if __name__ == "__main__":
    with sync_playwright() as p:
        IAM_test(p)
