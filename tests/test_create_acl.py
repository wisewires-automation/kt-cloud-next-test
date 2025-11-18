from pages.acl_page import ACLPage

def test_create_ig(project_opened_page, log):
    """
    Network ACL 생성 테스트
    """
    page = project_opened_page

    acl_page = ACLPage(page)

    log.info("Network ACL 생성 팝업 오픈")
    acl_page.open_acl_create()

    log.info("Network ACL 생성 시작")
    acl_name = acl_page.create_acl()

    log.info("Network ACL 생성 완료 | Network ACL 이름=%s", acl_name)
