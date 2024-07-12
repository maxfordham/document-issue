import pathlib
import sys
import xlwings as xw
import shutil


FDIR_MODULE = pathlib.Path(__file__).parent.parent / "src" / "issue_sheet"
sys.path.append(str(FDIR_MODULE))
FDIR_TEST_OUTPUTS = pathlib.Path(__file__).parent / "outputs"

FPTH_DNG = pathlib.Path(__file__).parent.parent / "xl" / "DocumentNumberGenerator.xlsm"
xw.Book(str(FPTH_DNG)).set_mock_caller()

from d_i_read_excel import read_excel
from constants import CONFIG_DIR

PROJECT_NUMBER = "J3870"
FDIR_DATA_PACKAGE = pathlib.Path(CONFIG_DIR) / PROJECT_NUMBER


def test_read_excel():
    if FDIR_DATA_PACKAGE.is_dir():
        shutil.rmtree(FDIR_DATA_PACKAGE)
    FDIR_DATA_PACKAGE.mkdir(exist_ok=True)
    (
        lookup,
        projectinfo,
        config,
        data,
        li_issues,
        doc_currentrevs,
        doc_descriptions,
        doc_issues,
        doc_distribution,
    ) = read_excel()
    assert (FDIR_DATA_PACKAGE / "datapackage.yaml").exists()
    print("done")
