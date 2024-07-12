import pathlib

FDIR_TESTS = pathlib.Path(__file__).parent
FDIR_TEST_OUTPUT = FDIR_TESTS / "testoutput"
FPTH_TITLE_BLOCK_PDF = FDIR_TEST_OUTPUT / "title-block.pdf"
FPTH_TITLE_BLOCK_PDF_NOMENCLATURE = (
    FDIR_TEST_OUTPUT / "title-block-name-nomenclature.pdf"
)
FPTH_TITLE_BLOCK_PDF_A3 = FDIR_TEST_OUTPUT / "title-block-a3.pdf"
FPTH_SCHEDULE_TITLE_PAGE_PDF = FDIR_TEST_OUTPUT / "title-page.pdf"
