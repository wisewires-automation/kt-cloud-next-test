"""
logger.py

테스트 코드/스크립트 전역에서 사용할 로깅 설정 모듈.

- setup_logging():
    * 루트 로거에 콘솔 핸들러와 회전 로그 파일 핸들러를 설정한다.
    * 콘솔: INFO 이상
    * 파일: DEBUG 이상, logs/test.log 에 기록

- get_logger(name, **context):
    * 이름(name)과 추가 컨텍스트를 가진 LoggerAdapter 를 반환한다.
    * extra 컨텍스트는 "%(key)s" 형태로 포맷터에서 참조 가능하다.
"""

import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging() -> None:
    """
    전체 애플리케이션 공용 로깅 설정을 초기화

    동작:
        - logs 디렉토리가 없으면 생성
        - 루트 로거(root logger)의 로그 레벨을 DEBUG 로 설정
        - 콘솔(StreamHandler)
            * 레벨: INFO
            * 포맷: "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        - 파일(RotatingFileHandler - logs/test.log)
            * 레벨: DEBUG
            * 최대 크기: 5MB
            * 백업 개수: 3개
            * 인코딩: utf-8
    """
    os.makedirs("logs", exist_ok=True)

    root = logging.getLogger()

    # 이미 핸들러가 설정되어 있으면 재설정하지 않음 (중복 로그 방지)
    if root.handlers:
        return

    root.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # 콘솔 핸들러: INFO 이상만 출력
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    root.addHandler(ch)

    # 파일 핸들러: DEBUG 이상 로그를 회전 파일로 저장
    fh = RotatingFileHandler(
        "logs/test.log",
        maxBytes=5_000_000,   # 5MB 초과 시 새 파일로 회전
        backupCount=3,        # 최대 3개까지 백업 보관 (test.log.1, test.log.2, ...)
        encoding="utf-8",
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    root.addHandler(fh)


def get_logger(name: str, **context) -> logging.LoggerAdapter:
    """
    주어진 이름(name)과 추가 컨텍스트(context)를 가진 LoggerAdapter를 반환

    Args:
        name (str):
            로거 이름. 일반적으로 모듈명이나 기능명 등을 사용.
        **context:
            로그 레코드에 함께 실을 추가 컨텍스트 키워드 인자들.
            예: user_id="admin", project="QA_TEST"

    Returns:
        logging.LoggerAdapter:
            logging.getLogger(name)을 기반으로 extra=context 를 포함한 LoggerAdapter 인스턴스.

    사용 예시:
        log = get_logger("login", user_id="admin")
        log.info("로그인 성공")
        # 포맷터에서 %(user_id)s 를 사용하면 컨텍스트가 함께 출력됨.
    """
    base = logging.getLogger(name)
    return logging.LoggerAdapter(base, extra=context)
