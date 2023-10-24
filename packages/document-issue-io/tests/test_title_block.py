from document_issue_io.title_block import build_title_block_pdf, build_schedule_title_page_template_pdf

from tests.constants import FDIR_TEST_OUTPUT


def test_build_title_block_pdf():
    FPTH_TITLE_BLOCK_PDF = FDIR_TEST_OUTPUT / "title-block.pdf"
    FPTH_TITLE_BLOCK_PDF.unlink(missing_ok=True)
    project_info = {
        "project_name": "A Max Fordham Project",
        "job_number": "J4321",
        "project_leader": "OH",
        "document_name": "06667-MXF-XX-XX-SH-M-20003",
        "document_description": "A description of the document that is important",
        "name_nomenclature": "project-originator-volume-level-type-role-number",
        "revision": "P01",
        "status_code": "S2",
        "status_description": "Suitable for information",
        "date": "2023-10-20"
    }
    build_title_block_pdf(project_info=project_info, fpth_output=FPTH_TITLE_BLOCK_PDF)
    assert FPTH_TITLE_BLOCK_PDF.exists()
    

def test_build_schedule_title_page_template_pdf():
    FPTH_SCHEDULE_TITLE_PAGE_PDF = FDIR_TEST_OUTPUT / "title-page.pdf"
    FPTH_SCHEDULE_TITLE_PAGE_PDF.unlink(missing_ok=True)
    project_info = {
        "project_name": "A Max Fordham Project",
        "job_number": "J4321",
        "project_leader": "OH",
        "document_name": "06667-MXF-XX-XX-SH-M-20003",
        "document_description": "A description of the document that is important",
        "name_nomenclature": "project-originator-volume-level-type-role-number",
        "revision": "P01",
        "status_code": "S2",
        "status_description": "Suitable for information",
        "date": "2023-10-20"
    }
    build_schedule_title_page_template_pdf(project_info=project_info, fpth_output=FPTH_SCHEDULE_TITLE_PAGE_PDF)
    assert FPTH_SCHEDULE_TITLE_PAGE_PDF.exists()