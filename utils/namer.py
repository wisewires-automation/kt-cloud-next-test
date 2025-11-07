import random
import string
from datetime import datetime

def unique_suffix(length: int = 4, alphabet: str = string.ascii_uppercase + string.digits) -> str:
    """영문 대문자+숫자 조합의 짧은 랜덤 접미사 생성"""
    return ''.join(random.choice(alphabet) for _ in range(length))

def make_name(prefix: str, suffix_len: int = 4, with_date: bool = False) -> str:
    """
    접두사 + (옵션)날짜 + 랜덤 접미사로 고유 이름 생성
    - with_date=False (예: TEST_PROJECT_AB12)
    - with_date=True (예: TEST_PROJECT_20251107_AB12)
    """
    suf = unique_suffix(suffix_len)
    if with_date:
        stamp = datetime.now().strftime('%Y%m%d')
        return f"{prefix}{stamp}_{suf}"
    return f"{prefix}{suf}"