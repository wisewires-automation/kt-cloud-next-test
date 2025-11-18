from pages.volume_page import VolumePage

def test_create_volume(project_opened_page, log):
    """
    Volume 생성 테스트
    """
    page = project_opened_page

    volume_page = VolumePage(page)

    log.info("Volume 생성 시작")
    volume_name = volume_page.create_volume()

    log.info("Volume 생성 완료 | Volume 이름=%s", volume_name)
