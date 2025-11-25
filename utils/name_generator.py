import random
import string

def generate_name(
    prefix: str,
    suffix_len: int = 4,
    letters_only: bool = False,
    letter_case: str = "upper",
) -> str:
    """
    접두사 + 랜덤 접미사로 고유 이름 생성

    - letters_only=False: 영문 + 숫자 (예: TEST_PROJECT_A9F2)
    - letters_only=True : 영문만      (예: TEST_PROJECT_ABCD)

    - letter_case="upper": 대문자 사용 (기본값)
    - letter_case="lower": 소문자 사용
    """
    # letter_case 검증
    if letter_case not in ("upper", "lower"):
        raise ValueError('letter_case must be "upper" or "lower"')

    # 대/소문자 알파벳 선택
    if letter_case == "upper":
        letters = string.ascii_uppercase
    else:
        letters = string.ascii_lowercase

    # 숫자 포함 여부
    if letters_only:
        alphabet = letters
    else:
        alphabet = letters + string.digits

    suffix = ''.join(random.choice(alphabet) for _ in range(suffix_len))
    return f"{prefix}{suffix}"