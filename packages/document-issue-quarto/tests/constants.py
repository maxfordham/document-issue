import pathlib

FDIR_ROOT = pathlib.Path(__file__).parent.parent
FDIR_TESTS = FDIR_ROOT / "tests"
FDIR_TEST_OUTPUT = FDIR_TESTS / "test-outputs"
FDIR_TEST_OUTPUT.mkdir(exist_ok=True)
FDIR_TEST_OUTPUT_DOC_ISSUE_NOTE = FDIR_TEST_OUTPUT / "document-issue-note"
FDIR_TEST_OUTPUT_DOC_ISSUE_NOTE.mkdir(exist_ok=True)
FDIR_TEST_OUTPUT_DOC_ISSUE_REPORT = FDIR_TEST_OUTPUT / "document-issue-report"
FDIR_TEST_OUTPUT_DOC_ISSUE_REPORT.mkdir(exist_ok=True)

FDIR_EXAMPLES = FDIR_TESTS / "examples"
FDIR_EXAMPLES_DOC_ISSUE_NOTE = FDIR_EXAMPLES / "document-issue-note"
FDIR_EXAMPLES_DOC_ISSUE_REPORT = FDIR_EXAMPLES / "document-issue-report"
