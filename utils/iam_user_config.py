import json
from pathlib import Path

DEFAULT_CONFIG_PATH = Path("config/iam_project_role.json")

def load_iam_users(config_path: str | Path = DEFAULT_CONFIG_PATH) -> dict:
    """
    config/iam_project_role.json 을 읽어서 role -> user_info 딕셔너리 반환
    """
    path = Path(config_path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_iam_user(role: str = "TEMP", config_path: str | Path = DEFAULT_CONFIG_PATH) -> dict:
    """
    특정 role 키에 해당하는 IAM 유저 정보 반환
    """
    iam_users = load_iam_users(config_path)
    return iam_users[role]
