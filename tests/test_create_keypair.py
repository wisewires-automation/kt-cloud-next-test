from pages.keypair_page import KeypairPage

def test_create_keypair(project_opened_page, log):
    page = project_opened_page

    # Key Pair 생성
    log.info("Key Pair 생성 시작")
    kp_page = KeypairPage(page)
    kp_name = kp_page.create_vpc()
    log.info("Key Pair 생성 완료 | Key Pair 이름=%s", kp_name)
