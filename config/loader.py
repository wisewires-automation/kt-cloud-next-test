from pathlib import Path
from typing import Any, Dict
import yaml

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

def _load_yaml(name: str) -> Dict[str, Any]:
    """
    config/data/{name}.yml 파일을 읽어서 dict로 반환
    예: name="users" -> data/users.yml
    """
    path = DATA_DIR / f"{name}.yml"
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    if not isinstance(data, dict):
        raise ValueError(f"Invalid format in {path}, expected mapping at root")
    return data


# 캐싱 (테스트 중 매번 디스크 읽지 않도록)
_CACHE: Dict[str, Dict[str, Any]] = {}


def _get_table(table: str) -> Dict[str, Any]:
    if table not in _CACHE:
        _CACHE[table] = _load_yaml(table)
    return _CACHE[table]


def get_user(key: str) -> Dict[str, Any]:
    """유저 데이터 가져오기"""
    users = _get_table("users")
    try:
        return users[key]
    except KeyError:
        raise KeyError(f"[users.yml] key '{key}' not found")


def get_project(key: str) -> Dict[str, Any]:
    """프로젝트 데이터 가져오기"""
    projects = _get_table("projects")
    try:
        return projects[key]
    except KeyError:
        raise KeyError(f"[projects.yml] key '{key}' not found")


def get_vpc(key: str) -> Dict[str, Any]:
    """VPC 데이터 가져오기"""
    vpcs = _get_table("vpcs")
    try:
        return vpcs[key]
    except KeyError:
        raise KeyError(f"[vpcs.yml] key '{key}' not found")
