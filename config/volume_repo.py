from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any

import yaml


CONFIG_PATH = Path(__file__).resolve().parent / "data" / "volumes.yml"


@dataclass
class VolumeConfig:
    key: str
    name: str
    description: str
    type_index: int   # 0 ~ 2
    size: str      # 8의 배수
    zone_index: int   # 0 고정


class VolumeRepository:
    def __init__(self, path: Path = CONFIG_PATH):
        self._path = path
        self._volumes: Dict[str, VolumeConfig] = {}
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            self._volumes = {}
            return

        with self._path.open(encoding="utf-8") as f:
            raw: Dict[str, Any] = yaml.safe_load(f) or {}

        volumes: Dict[str, VolumeConfig] = {}

        for key, value in raw.items():
            # 필드 파싱
            name = value["name"]
            description = value.get("description", "")
            type_index = int(value["type_index"])
            size = value["size"]
            zone_index = int(value.get("zone_index", 0))

            volumes[key] = VolumeConfig(
                key=key,
                name=name,
                description=description,
                type_index=type_index,
                size=size,
                zone_index=zone_index,
            )

        self._volumes = volumes

    def get(self, key: str) -> VolumeConfig:
        try:
            return self._volumes[key]
        except KeyError:
            raise KeyError(f"[VolumeRepository] Unknown volume key: {key!r}")

    def all(self):
        return list(self._volumes.values())


volume_repo = VolumeRepository()
