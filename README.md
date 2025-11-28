# KT Cloud 콘솔 자동화 테스트

Playwright + Page Object Model(POM) 구조로 작성한 프로젝트입니다.

---

## 1. 기술 스택

- Python 3.11
- [Playwright for Python](https://playwright.dev/python/)


## 2. 개발 환경 / 사전 준비

### 2.1. Python 가상환경 생성
프로젝트 루트에서 가상환경을 생성합니다
```bash
python -m venv .venv
```

#### 가상환경 활성화
```bash
# Windows
.venv\Scripts\Activate.ps1 

# macOS / Linux
source .venv/bin/activate 
```

### 2.2. 패키지 설치
```bash
pip install -r requirements.txt
playwright install
```

## 3. 환경변수 설정
루트 디렉터리에 **.env** 파일을 생성하고 아래 항목을 설정합니다.
```ini
# 로그인 URL
LOGIN_URL=https://console.ktcloud.com/...

# 로그인 정보
KT_USER_ID=your_kt_id
KT_USER_PW=your_kt_password

GROUP_ID=your_group_id
IAM_USER_ID=your_iam_id
IAM_USER_PW=your_iam_password

# 스크린샷 경로
SCREENSHOT_PATH = C:\\
```

## 4. 프로젝트 구조
```
KT-CLOUD-CONSOLE/
├─ config/                      # 테스트용 설정 로더 (repo)
│  ├─ project_repo.py           # 프로젝트 설정 로더
│  └─ ...                       # 기타 설정 로더
│
├─ data/                        # YAML 기반 테스트 정의
│  ├─ projects.yml
│  └─ ...
│
├─ pages/                       # Playwright Page Object 모음                # 
│  ├─ common.py   
│  ├─ actions.py                # 공통 locator
│  ├─ auth_page.py              # 로그인 / 로그아웃 POM
│  └─ ...                       # 기타 페이지들
│
├─ tests/                       # 테스트 스크립트 모음
│  ├─ test_auth.py              # 로그인 관련 시나리오
│  └─ ...                       # 기타 테스트 케이스들
│
├─ utils/
│  ├─ screenshot.py              # 스크린샷 유틸
│  ├─ logger.py                  # 공통 로깅 설정 (logs/test.log 등)
│  ├─ name_generator.py          # 랜덤 이름 생성 유틸
│  └─ playwright_helpers.py      # Playwright 세션/로그인 헬퍼
│
├─ logs/                         # 로깅 출력 디렉터리
├─ .env                          # 환경변수 설정 파일
├─ .env.example                  # .env 템플릿 (선택)
├─ requirements.txt
├─ .gitignore
└─ README.md
```

## 5. 테스트 실행 방법
각 테스트 모듈을 ``python -m`` 방식으로 실행합니다.

```
# 예시
python -m tests.test_auth
python -m tests.test_project
```

모든 테스트 코드는 ``tests/`` 디렉터리 아래에 위치합니다

### 5.1. 공통 Playwright 헬퍼
``create_page(headless: bool = False)``

→ ``with create_page() as page:`` 형태로 Playwright page 객체 생성
```
# tests/test_auth.py (예시)

from utils.playwright_helpers import create_page, login_as_admin

def main():
    with create_page(headless=False) as page:
        login_as_admin(page)
        # 이후 필요한 검증 및 추가 시나리오 수행

if __name__ == "__main__":
    main()
```

## 6. 기타
- 스크린샷
    - 오류 발생 시 ``utils/screenshot.py``에서 스크린샷을 남길 수 있습니다.

- 로깅
    - ``utils/logger.py``의 ``setup_logging()`` / ``get_logger()``를 통해
모듈별 로거를 생성해 ``logs/`` 디렉터리에 로그를 남깁니다.