"""
logger.py에서 설정한 로깅은 콘솔 출력과 logs/test.log 파일에 함께 기록됨
"""
import logging, os
from logging.handlers import RotatingFileHandler

def setup_logging():
    os.makedirs("logs", exist_ok=True)
    root = logging.getLogger()
    if root.handlers:  # 중복 방지
        return
    root.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    root.addHandler(ch)

    fh = RotatingFileHandler("logs/test.log", maxBytes=5_000_000, backupCount=3, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    root.addHandler(fh)

def get_logger(name: str, **context):
    base = logging.getLogger(name)
    return logging.LoggerAdapter(base, extra=context)
