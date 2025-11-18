import random, string
from datetime import datetime

def random_alpha_num(length: int = 4, alphabet: str = string.ascii_uppercase + string.digits) -> str:
    """영문 대문자+숫자 조합 랜덤 접미사 생성"""
    return ''.join(random.choice(alphabet) for _ in range(length))

def random_alpha(length: int = 4) -> str:
    """숫자 없이 영문 대문자만 랜덤 접미사 생성"""
    return random_alpha_num(length=length, alphabet=string.ascii_uppercase)

def make_name(prefix: str, suffix_len: int = 4, with_date: bool = False) -> str:
    """
    접두사 + (옵션)날짜 + 랜덤 접미사로 고유 이름 생성
    - with_date=False (예: TEST_PROJECT_AB12)
    - with_date=True (예: TEST_PROJECT_20251107_AB12)
    """
    suf = random_alpha_num(suffix_len)
    if with_date:
        stamp = datetime.now().strftime('%Y%m%d')
        return f"{prefix}{stamp}_{suf}"
    return f"{prefix}{suf}"

def make_name_only_alpha(prefix: str, suffix_len: int = 4) -> str:
    """접두사 + 영문 대문자 랜덤 접미사"""
    suf = random_alpha(suffix_len)
    return f"{prefix}{suf}"