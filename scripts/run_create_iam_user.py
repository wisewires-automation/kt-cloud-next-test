from utils.logger import setup_logging, get_logger
from utils.playwright_helpers import create_page, login_as_admin
from scenarios.iam_user_scenarios import create_iam_user_scenario
from utils.iam_user_config import get_iam_user

def main():
    setup_logging()
    log = get_logger("run_create_iam_user")

    iam_user_info = get_iam_user("TEMP")
    log.info(
        "[SCRIPT] 생성 예정 IAM 계정 | role=TEMP, id=%s, name=%s",
        iam_user_info["id"],
        iam_user_info["name"],
    )

    with create_page(headless=False) as page:
        login_as_admin(page, log)

        created_id = create_iam_user_scenario(page, iam_user_info, log)
        log.info("[SCRIPT] IAM 사용자 생성 완료 | id=%s", created_id)

if __name__ == "__main__":
    main()
