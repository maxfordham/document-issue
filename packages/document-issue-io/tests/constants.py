import pathlib

FDIR_TESTS = pathlib.Path(__file__).parent
FDIR_TEST_OUTPUT = FDIR_TESTS / "test-outputs"
FPTH_TITLE_BLOCK_PDF = FDIR_TEST_OUTPUT / "title-block.pdf"
FPTH_TITLE_BLOCK_PDF_NOMENCLATURE = (
    FDIR_TEST_OUTPUT / "title-block-name-nomenclature.pdf"
)
FPTH_TITLE_BLOCK_PDF_A3 = FDIR_TEST_OUTPUT / "title-block-a3.pdf"
FPTH_SCHEDULE_TITLE_PAGE_PDF = FDIR_TEST_OUTPUT / "title-page.pdf"


# title block / page
(
    TITLE_BLOCK_A4_P,
    TITLE_BLOCK_A4_P_CUSTOM_NOMENCLATURE,
    TITLE_PAGE_A4_P,
    TITLE_BLOCK_A3_L,
    TITLE_PAGE_A3_L,
) = (
    "title-block-a4-p",
    "title-block-a4-p-custom-nomenclature",
    "title-page-a4-p",
    "title-block-a3-l",
    "title-page-a3-l",
)



# report outputs
# "report-a4-p"
# "report-a4-p-many-notes-and-issues"
# "report-a4-p-with-author"
# "report-a4-p-with-author-and-checker"
# "report-a4-p-with-markdown-content"
# "report-a3-l"

# design note outputs
# "note-a4-p"
# "note-a3-l"

# issue sheets
