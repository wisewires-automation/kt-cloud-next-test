from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any
import yaml

CONFIG_PATH = Path(__file__).resolve().parent.parent / "data" / "security_groups.yml"


@dataclass
class SGConfig:
    key: str
    name: str
    description: str
    provision: str


class SGRepository:
    def __init__(self, path: Path = CONFIG_PATH):
        self._path = path
        self._projects: Dict[str, SGConfig] = {}
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            self._projects = {}
            return

        with self._path.open(encoding="utf-8") as f:
            raw: Dict[str, Any] = yaml.safe_load(f) or {}

        self._projects = {
            key: SGConfig(
                key=key,
                name=value["name"],
                description=value.get("description", ""),
                provision=value.get("provision", "manual"),
            )
            for key, value in raw.items()
        }

    def get(self, key: str) -> SGConfig:
        try:
            return self._projects[key]
        except KeyError:
            raise KeyError(f"[SGRepository] Unknown project key: {key!r}")

    def all(self):
        return list(self._projects.values())


sg_repo = SGRepository()
