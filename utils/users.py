from dataclasses import dataclass
import json
from pathlib import Path
from typing import Dict

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "users.json"

@dataclass
class TestUser:
    key: str          # JSON 상의 키 (예: "SERVER_MANAGER")
    id: str
    name: str
    email: str
    phone: str
    password: str

class UserRepository:
    def __init__(self, path: Path = CONFIG_PATH):
        self._path = path
        self._users: Dict[str, TestUser] = {}
        self._load()

    def _load(self):
        with self._path.open(encoding="utf-8") as f:
            raw = json.load(f)

        self._users = {
            key: TestUser(
                key=key,
                id=value["id"],
                name=value["name"],
                email=value["email"],
                phone=value["phone"],
                password=value["password"],
            )
            for key, value in raw.items()
        }

    def get(self, key: str) -> TestUser:
        """
        역할 키로 사용자 가져오기 (예: "SERVER_MANAGER").
        """
        try:
            return self._users[key]
        except KeyError:
            raise KeyError(f"[UserRepository] Unknown user key: {key!r}")

    def all(self):
        return list(self._users.values())


# 전역 인스턴스 하나 만들어두고 import 해서 쓰는 용도
user_repo = UserRepository()
