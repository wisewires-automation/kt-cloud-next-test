# config/vpc_repo.py
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any
import yaml

CONFIG_PATH = Path(__file__).resolve().parent.parent / "data" / "vpcs.yml"


@dataclass
class VPCConfig:
    key: str
    name: str
    cidr: str
    project_key: str
    provision: str


class VPCRepository:
    def __init__(self, path: Path = CONFIG_PATH):
        self._path = path
        self._vpcs: Dict[str, VPCConfig] = {}
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            self._vpcs = {}
            return

        with self._path.open(encoding="utf-8") as f:
            raw: Dict[str, Any] = yaml.safe_load(f) or {}

        self._vpcs = {
            key: VPCConfig(
                key=key,
                name=value["name"],
                cidr=value["cidr"],
                project_key=value["project_key"],
                provision=value.get("provision", "auto"),
            )
            for key, value in raw.items()
        }

    def get(self, key: str) -> VPCConfig:
        try:
            return self._vpcs[key]
        except KeyError:
            raise KeyError(f"[VPCRepository] Unknown vpc key: {key!r}")

    def all(self):
        return list(self._vpcs.values())


vpc_repo = VPCRepository()
