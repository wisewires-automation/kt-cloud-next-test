import os
import pytest
from pages.auth_page import AuthPage
from dotenv import load_dotenv
import time

load_dotenv()

def test_auth(page):

    email = os.getenv("KT_EMAIL")
    password = os.getenv("KT_PASSWORD")
    url = os.getenv("KT_LOGIN_URL", "https://console.gcloud.kt.com")

    if not (email and password):
        pytest.skip("환경변수 KT_EMAIL, KT_PASSWORD를 설정해야 실행합니다.")
    
    auth = AuthPage(page)
    auth.login(url=url, email=email, password=password, timeout=10000)

    time.sleep(100)

    auth.logout()