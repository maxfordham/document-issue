import pathlib
import sys
import xlwings as xw

FDIR_MODULE = pathlib.Path(__file__).parent.parent / "src" / "issue_sheet"
sys.path.append(str(FDIR_MODULE))
FDIR_TEST_OUTPUTS = pathlib.Path(__file__).parent / "outputs"
FDIR_DATA_PACKAGE = FDIR_TEST_OUTPUTS / "datapackage"
FPTH_DNG = (
    pathlib.Path(__file__).parent.parent / "excel-dng" / "DocumentNumberGenerator.xlsm"
)
xw.Book(str(FPTH_DNG)).set_mock_caller()

from d_i_read_excel import read_excel
import shutil


def test_read_excel():
    shutil.rmtree(FDIR_DATA_PACKAGE)
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
    ) = read_excel(fdir_package=FDIR_DATA_PACKAGE)
    assert (FDIR_DATA_PACKAGE / "datapackage.yaml").exists()
    print("done")
