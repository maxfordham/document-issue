import pathlib

FDIR_FIND_FILES = pathlib.Path(__file__).parent / "data-processed"

def get_found_files():
    return list(FDIR_FIND_FILES.glob("found_files*.txt"))

def load_found_files(fpths):
    found = {}
    missing = {}
    for fpth in fpths:
        with open(fpth, "r") as file:
            lines = file.read().splitlines()
            _ = {(line.split(",", 2)[0], line.split(",", 2)[1]): line.split(",", 2)[2] for line in lines}
            found = found | {k: v for k, v in _.items() if v != ""}
            missing = missing | {k: v for k, v in _.items() if v == ""}

    for x in list(missing.keys()):
        if x in found.keys():
            missing.pop(x)

    return found, missing

