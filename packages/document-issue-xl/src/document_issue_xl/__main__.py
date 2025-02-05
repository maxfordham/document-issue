"""Created on Fri Feb  14 13:37:03 2019

@author: o.beckett
"""

import pathlib
import sys
from datetime import datetime

import xlwings as xw
from d_i_gui import run
from d_i_ui import warning_messagebox

gettime = lambda: datetime.now().strftime("%H-%M-%S")
getname = lambda: f"df_{gettime()}.csv"

if __name__ == "__main__":
    print(sys.argv)
    argv = sys.argv[1:]
    fpath = None
    if len(sys.argv) <= 1:
        cmd = run
    elif len(sys.argv) > 1:
        fpth = argv[-1]
        cmd = run

    if __debug__:
        print("Debug ON")
        fpth = pathlib.Path(__file__).parent.parent.parent / "xl" / "DocumentNumberGenerator-v0_0_12.xlsm"
        fpth = pathlib.Path(
            r"J:\J7004\Issue Sheet\Stage 4 - Construction\J7004_DocumentNumberGenerator_Construction.xlsm",
        )
        fpth = pathlib.Path(
            r"J:\J7081\Project Management\Job Running\J7081 Document Number Generator.xlsm",
        )
        fpth = pathlib.Path(__file__).parent.parent.parent / "xl" / "DocumentNumberGenerator-v0_0_7.xlsm"
        fpth = pathlib.Path(
            r"J:\J7561\Project Management\Job Running\J7561_DocumentNumberGenerator.xlsm",
        )  # done
        fpth = pathlib.Path(
            r"J:\J6962\Project Management\Job Running\Issue Sheets\MEP\J6962 DocumentNumberGenerator1.xlsm",
        )  # done
        fpth = pathlib.Path(
            r"J:\J7194\Project Management\Job Running\Issue Sheet\J7194 DocumentNumberGenerator1.xlsm",
        )  # darren - done
        fpth = pathlib.Path(
            r"J:\J7151\Project Management\Job Running\DocumentNumberGenerator - UPP 2.0 NEW BUILD and RF2 MASTER COPY.xlsm",
        )  # carys - done
        fpth = pathlib.Path(
            r"J:\J7236\Project Management\Job Running\J7236 DocumentNumberGenerator Issue Sheet.xlsm",
        )  # liz - duplicate doc names - done
        fpth = pathlib.Path(
            r"J:\J6246\Issue Sheets\6246 _Issue Sheet Document Numbers Register.xlsm",
        )  # stefan / anna - uniclass in doc name - done
        fpth = pathlib.Path(
            r"J:\J7516\Project Management\Job Running\Issue Sheet DNG\UoP DNG.xlsm",
        )  # holly - done
        fpth = pathlib.Path(
            r"J:\J6793\Issue Sheet\J6793 UOONHB Issue Sheet_Drawing Number Generator.xlsm",
        )  # cheryl - done
        fpth = pathlib.Path(__file__).parent.parent.parent / "xl" / "DocumentNumberGenerator.xlsm"
        fpth = pathlib.Path(
            r"J:\J6848\Project Management\Job Running\J6848 - Wembley Link Document Number Generator.xlsm",
        )  # cheryl - done
        fpth = pathlib.Path(
            r"J:\J7207\Project Management\Job Running\J7207 DocumentNumberGenerator.xlsm",
        )  # liz - done
        fpth = pathlib.Path(r"J:\J7595\Issue Sheet.xlsm")  # emma - done
        fpth = pathlib.Path(
            r"J:\J6771\Issue Sheet\6771 Issue Sheet_DocumentNumberGenerator.xlsm",
        )  # cheryl - done
        fpth = pathlib.Path(
            r"J:\J7160\Project Management\Job Running\J7160 Document Number Generator.xlsm",
        )  # liz - done
        fpth = pathlib.Path(
            r"J:\J6695\Issue Sheets\J6695 DocumentNumberGenerator -Phase 2 - 27.xlsm",
        )  # anna - done
        fpth = pathlib.Path(
            r"J:\J7262\Issue Sheet\7262 Issue Sheet.xlsm",
        )  # emma - done
        fpth = pathlib.Path(
            r"J:\J7081\Project Management\Job Running\J7081 Document Number Generator.xlsm",
        )  # moa - done
        fpth = pathlib.Path(
            r"J:\J6865\Project Management\Job Running\J6865 Document Number Generator.xlsm",
        )  # moa - WIP
        fpth = pathlib.Path(
            r"J:\J7568\Project Management\Job Running\J7568 Issue Sheet_DocumentNumberGenerator previously 6496.xlsm",
        )  # cheryl - done
        fpth = pathlib.Path(
            r"J:\J7286\Project Management\Job Running\J7286 Issue Sheet.xlsm",
        )  # liz - done
        fpth = pathlib.Path(
            r"J:\J6681\Issue sheets\J6681 CCCSC Engineer Document Number Generator Issue Sheet - Special CC only.xlsm",
        )  # holly - done
        fpth = pathlib.Path(
            r"J:\J6866\New\Issue Sheet\DocumentNumberGenerator1 stage 3 - USE.xlsm",
        )  # emma - done
        fpth = pathlib.Path(
            r"J:\J6866\New\Issue Sheet\DocumentNumberGenerator1 stage 3 - USE.xlsm",
        )  # emma - done
        fpth = pathlib.Path(
            r"J:\J6792\Project Management\Job Running\J6792_DocumentNumberGenerator.xlsm",
        )  # stefan - done
        fpth = pathlib.Path(
            r"J:\J6943\ISSUE SHEET\Main issue sheet - DocumentNumberGenerator.xlsm",
        )  # emma - done
        fpth = pathlib.Path(r"J:\J7500\J7500 Issue Sheet.xlsm")  # emma - done
        fpth = pathlib.Path(
            r"J:\J7536\Issue Sheet\J7536 - DocumentNumberGenerator.xlsm",
        )  # emma - done
        fpth = pathlib.Path(
            r"C:\engDev\git_mf\document-issue\packages\document-issue-xl\xl\DocumentNumberGenerator.xlsm",
        )  # JG testing
        fpth = pathlib.Path(
            r"J:\J6891\Project Management\Job Running\DocumentNumberGenerator J6891 Poole Museum.xlsm",
        )  # Anna - done
        fpth = pathlib.Path(
            r"J:\J7129\Project Management\Job Running\Issue Sheet\J7129 DocumentNumberGenerator.xlsm",
        )  # Tina - done
        fpth = pathlib.Path(
            r"J:\J7424\ISSUE\DocumentNumberGenerator - 7424.xlsm",
        )  # emma - done
        fpth = pathlib.Path(
            r"J:\J7294\Project Management\Job Running\J7294 Issue Sheet.xlsm",
        )  # anna - done
        fpth = pathlib.Path(
            r"J:\J6790\Project Management\Job Running\Issue Sheet\J6790 - Document Number Generator - Goods Office.xlsm",
        )  # anna - done
        fpth = pathlib.Path(
            r"J:\J7249\Project Management\Job Running\7249 DocumentNumber Issue Sheet - BSWN.xlsm",
        )
        fpth = pathlib.Path(
            r"J:\J7268\Project Management\Job Running\Issue Sheet\J7268 - DocumentNumberGenerator1.xlsm",
        )  # tina - done
        fpth = pathlib.Path(
            r"J:\J6372\Project Management\Job Running\J6372 G1 Document Number Generator.xlsm",
        )  # moa - done
        fpth = pathlib.Path(
            r"J:\J7595\Project Management\Job Running\J7595 Drawing Number Generator.xlsm",
        )  # tina, aidan
        fpth = pathlib.Path(
            r"J:\J7251\Project Management\Job Running\Issue Sheet\J7251 - DocumentNumberGenerator1.xlsm",
        )  # tina - done
        fpth = pathlib.Path(
            r"J:\J7081\Project Management\Job Running\J7081 Document Number Generator.xlsm",
        )  # moa - done
        fpth = pathlib.Path(
            r"J:\J7360\ISSUE\DNG\J7360-MXF-XX-XX-IS-J-00000.xlsm",
        )  # emma - done - same date issue
        fpth = pathlib.Path(
            r"J:\J6378\Project Management\Job Running\6378 MWP DNG.xlsm",
        )  # holly - done
        fpth = pathlib.Path(
            r"J:\J7045\ISSUE SHEET\J7045 Ruskin -new issue sheet 20241202-JGedit.xlsm",
        )  # emma - done

        fpth = pathlib.Path(
            r"J:\J7251\Project Management\Job Running\Issue Sheet\J7251 - DocumentNumberGenerator1 - V2.xlsm",
        )  # tina - done

        fpth = pathlib.Path(
            r"J:\J6771\Issue Sheet\6771 Issue Sheet_DocumentNumberGenerator.xlsm",
        )  # cheryl - done

        # --- LOCAL DEV ---
        # fpth = pathlib.Path(__file__).parent.parent.parent / "xl" / "DocumentNumberGenerator.xlsm"
        # ---

        xw.Book(str(fpth)).set_mock_caller()
        RESULTS = cmd()
    else:
        print("Release Mode")
        try:
            if fpath is not None:
                xw.Book(fpath).set_mock_caller()
            RESULT = cmd()
        except Exception as exc:
            warning_messagebox(message=exc, title="PDF ERROR")
