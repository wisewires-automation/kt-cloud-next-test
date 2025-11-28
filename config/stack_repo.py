# config/stack_repo.py
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List
import yaml

CONFIG_PATH = Path(__file__).resolve().parent / "data" / "stacks.yml"


@dataclass
class StackConfig:
    key: str
    description: str
    project_key: str
    vpc_key: str
    subnet_key: str


class StackRepository:
    def __init__(self, path: Path = CONFIG_PATH):
        self._path = path
        self._stacks: Dict[str, StackConfig] = {}
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            self._stacks = {}
            return

        with self._path.open(encoding="utf-8") as f:
            raw: Dict[str, Any] = yaml.safe_load(f) or {}

        self._stacks = {}
        for key, value in raw.items():
            # subnet_list = value.get("subnets", [])
            self._stacks[key] = StackConfig(
                key=key,
                description=value.get("description", ""),
                project_key=value["project_key"],
                vpc_key=value["vpc_key"],
                subnet_key=value["subnet_key"]
            )

    def get(self, key: str) -> StackConfig:
        try:
            return self._stacks[key]
        except KeyError:
            raise KeyError(f"[StackRepository] Unknown stack key: {key!r}")

    def all(self):
        return list(self._stacks.values())


stack_repo = StackRepository()
