from pages.volume_page import VolumePage

def test_create_volume(project_opened_page, log):
    page = project_opened_page

    # Volume 생성
    log.info("Volume 생성 시작")
    volume_page = VolumePage(page)
    volume_name = volume_page.create_volume()
    log.info("Volume 생성 완료 | Volume 이름=%s", volume_name)
