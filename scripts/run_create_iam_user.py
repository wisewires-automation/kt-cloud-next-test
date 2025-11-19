from utils.logger import setup_logging, get_logger
from utils.playwright_helpers import create_page, login_as_admin
from utils.iam_user_config import get_iam_user
from utils.capture import ScreenshotSession
from scenarios.iam_user_scenarios import create_iam_user_scenario

log = get_logger("run_create_iam_user")

def main():

    iam_user_info = get_iam_user("TEMP")

    log.info("생성 예정 IAM 계정 | role=TEMP, id=%s",iam_user_info["id"],)

    with create_page(headless=False) as page, \
        ScreenshotSession(__file__, zip_name="run_create_iam_user") as sc:

        try:
            login_as_admin(page, log)
            create_iam_user_scenario(page, log, iam_user_info, sc=sc)
        except Exception:
            sc.snap(page, "error")
            log.exception("[ERROR] IAM 계정 생성 중 예외 발생")
            raise

if __name__ == "__main__":
    main()
