from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any
import yaml

CONFIG_PATH = Path(__file__).resolve().parent / "data" / "subnets.yml"


@dataclass
class SubnetConfig:
    key: str
    name: str
    cidr: str
    vpc_key: str
    project_key: str
    zone: str
    type: str
    provision: str


class SubnetRepository:
    def __init__(self, path: Path = CONFIG_PATH):
        self._path = path
        self._subnets: Dict[str, SubnetConfig] = {}
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            self._subnets = {}
            return

        with self._path.open(encoding="utf-8") as f:
            raw: Dict[str, Any] = yaml.safe_load(f) or {}

        self._subnets = {
            key: SubnetConfig(
                key=key,
                name=value["name"],
                cidr=value["cidr"],
                vpc_key=value["vpc_key"],
                project_key=value["project_key"],
                zone=value.get("zone", ""),
                type=value.get("type", ""),
                provision=value.get("provision", "auto"),
            )
            for key, value in raw.items()
        }

    def get(self, key: str) -> SubnetConfig:
        try:
            return self._subnets[key]
        except KeyError:
            raise KeyError(f"[SubnetRepository] Unknown subnet key: {key!r}")

    def all(self):
        return list(self._subnets.values())


subnet_repo = SubnetRepository()
