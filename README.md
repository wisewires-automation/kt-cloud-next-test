# KT Cloud 자동화 테스트

Playwright + Pytest + Page Object Model(POM) 구조로 자동화한 테스트 프로젝트입니다.

---

## 1. 기술 스택

- Python 3.11 (권장)
- [Playwright for Python](https://playwright.dev/python/)
- Pytest


## 2. 개발 환경 / 사전 준비

### 2.1. Python 가상환경 생성
#### 프로젝트 루트에 가상환경 생성
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

# KT Cloud 계정
KT_USER_ID=your_kt_id
KT_USER_PW=your_kt_password

# IAM 계정
GROUP_ID=your_group_id
IAM_USER_ID=your_iam_id
IAM_USER_PW=your_iam_password

# VPC / Subnet / Server 관련 값
VPC_CIDR=10.0.0.0/8
PROJECT_NAME=TEST_CREATE_SERVER
```

## 4. 프로젝트 구조
```
KT-CLOUD-CONSOLE/
├─ pages/                      # Playwright Page Object 모음
│  ├─ auth_page.py             # 로그인 / 로그아웃 POM
│  └─ ...                      # 기타 페이지들
│
├─ tests/                      # Pytest 테스트 스위트
│  ├─ test_auth.py             # 로그인 테스트
│  └─ ...                      # 기타 테스트 케이스들
│
├─ utils/
│  ├─ namer.py            # 랜덤 이름 생성 유틸
│  ├─ logger.py           # 공통 로깅 설정 유틸 (logs/test.log 에 기록)
│
├─ logs/                  # logger용 로그 파일 디렉터리
│
├─ .env                   # 환경변수 설정
├─ .env.example           # 예시 환경변수 템플릿 (선택)
├─ requirements.txt
├─ pytest.ini             # pytest 설정 (선택)
└─ README.md
```

## 5. 테스트 실행 방법

### 5.1. 전체 테스트 실행
```
pytest
```

### 5.2. 특정 파일만 실행
```
pytest tests/test_auth.py
```

### 5.3. 특정 테스트 함수만 실행

```
# IAM 로그인만 실행
pytest tests/test_auth.py::test_iam_login
```

### 5.4. 키워드로 실행
```
# 이름에 "vpc"가 포함된 테스트만 실행
pytest -k "vpc"
```