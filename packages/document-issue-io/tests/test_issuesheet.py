from document_issue_io.issuesheet import write_issuesheet_and_issuehistory
import pathlib

FDIR_TESTS = pathlib.Path(__file__).parent
FDIR_DATAPACKAGE = FDIR_TESTS / "datapackage"
FDIR_DATAPACKAGE_CUSTOM = FDIR_TESTS / "datapackage-custom-nomenclature"
FDIR_DATAPACKAGE_OLD = FDIR_TESTS / "datapackage-xl-v0_0_12"
FDIR_TESTOUTPUT = FDIR_TESTS / "testoutput"


def run_issue_sheet_tests(fdir_datapackage, glob_str):
    fpths = list(FDIR_TESTOUTPUT.glob(glob_str))
    for l in fpths:
        l.unlink(missing_ok=True)
    fpth_issuesheet, fpths_issuehistory = write_issuesheet_and_issuehistory(
        fdir_datapackage
    )
    assert fpth_issuesheet.exists()
    assert all(fpth.exists() for fpth in fpths_issuehistory)
    print("done")
    return fpth_issuesheet, fpths_issuehistory


def test_write_issuesheet_and_issuehistory():
    fpth_issuesheet, fpths_issuehistory = run_issue_sheet_tests(
        FDIR_DATAPACKAGE, "03870-MXF*-IS-J-*.pdf"
    )


def test_write_issuesheet_and_issuehistory_with_custom_nomenclature():
    # the naming nomenclature in `projectinfo.json` is:
    # "originator - project - volume - level - infotype - role - number"
    fpth_issuesheet, fpths_issuehistory = run_issue_sheet_tests(
        FDIR_DATAPACKAGE_CUSTOM, "MXF-03870*-IS-J-*.pdf"
    )
    assert fpth_issuesheet.stem[0:3] == "MXF"
    print("done")


def test_write_issuesheet_and_issuehistory_with_old_dng_data():
    # the naming nomenclature in `projectinfo.json` is:
    # "originator - project - volume - level - infotype - role - number"
    fpth_issuesheet, fpths_issuehistory = run_issue_sheet_tests(
        FDIR_DATAPACKAGE_OLD, "04321-MXF*-IS-J-*.pdf"
    )
