from document_issue_io.issuesheet import write_issuesheet_and_issuehistory
import pathlib

FDIR_TESTS = pathlib.Path(__file__).parent
FDIR_DATAPACKAGE = FDIR_TESTS / "datapackage"
FDIR_DATAPACKAGE_CUSTOM = FDIR_TESTS / "datapackage-custom-nomenclature"
FDIR_TESTOUTPUT = FDIR_TESTS / "testoutput"


def test_write_issuesheet_and_issuehistory():
    fpths = list(FDIR_TESTOUTPUT.glob("*-IS-J-*.pdf"))
    for l in fpths:
        l.unlink(missing_ok=True)
    fpth_issuesheet, fpths_issuehistory = write_issuesheet_and_issuehistory(
        FDIR_DATAPACKAGE
    )
    assert fpth_issuesheet.exists()
    assert all(fpth.exists() for fpth in fpths_issuehistory)
    print("done")


def test_write_issuesheet_and_issuehistory_with_custom_nomenclature():
    # the naming nomenclature in `projectinfo.json` is:
    # "originator - project - volume - level - infotype - role - number"
    fpths = list(FDIR_DATAPACKAGE_CUSTOM.glob("*-IS-J-*.pdf"))
    for l in fpths:
        l.unlink(missing_ok=True)
    fpth_issuesheet, fpths_issuehistory = write_issuesheet_and_issuehistory(
        FDIR_DATAPACKAGE_CUSTOM
    )
    assert fpth_issuesheet.exists()
    assert all(fpth.exists() for fpth in fpths_issuehistory)
    assert fpth_issuesheet.stem[0:3] == "MXF"
    print("done")
