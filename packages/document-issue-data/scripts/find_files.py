import glob
import pathlib
from datetime import datetime

from _load_found_files import load_found_files, get_found_files, FDIR_FIND_FILES
from _load_dng_data import get_issues, get_docs, FDIR_RAW


FDIR_JDRIVE = pathlib.Path("~/jobs").expanduser()
FPTH_MESSAGE = pathlib.Path(__file__).parent / "findfiles-message.txt"


def datetime_string():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")



def save_found_files(found_files, fpth):
    with open(fpth, "w") as file:
        for (document_code, date), file_path in found_files.items():
            file.write(f"{document_code},{date},{file_path}\n")


def search_files(df_issues, ignore_missing=True):
    fpths = get_found_files()
    # Load already found files
    found, missing = load_found_files(fpths)
    fpth_save = FDIR_FIND_FILES / f"found_files_{str(len(list(fpths)) + 1)}.txt"
    found_files_dict = {}  # found within this session

    # Get unique combinations of project numbers, document codes, and dates
    unique_combinations = df_issues[["project_number", "document_code", "date"]].drop_duplicates()

    for _, row in unique_combinations.iterrows():
        project_number = row["project_number"]
        document_code = row["document_code"]
        if "\n" in document_code:
            document_code = document_code.replace("\n", "")
        date = row["date"]

        # Skip if document_code and date are already found
        if (document_code, date) in found:
            continue

        if ignore_missing:
            if (document_code, date) in missing:
                continue

        # Construct directory path
        project_dir = FDIR_JDRIVE / f"J{project_number}/Outgoing/{date}*"

        # Search for directories matching the project pattern
        project_dirs = glob.glob(str(project_dir))

        file_found = False
        for dir in project_dirs:
            # Search for files with document_code in the file name
            search_pattern = f"{dir}/**/*{document_code}*"
            files = glob.glob(search_pattern, recursive=True)
            if files:
                for file in files:
                    found_files_dict[(document_code, date)] = file
                file_found = True
                break

        if not file_found:
            found_files_dict[(document_code, date)] = ""

        save_found_files(found_files_dict, fpth_save)

    # Save found files after every found file or not found
    if len(found_files_dict) == 0:
        fpth_save = None
        m = f"{datetime_string()}: no new files found"
        print(m)
        FPTH_MESSAGE.write_text(m)

    return fpth_save


# Example usage
df_issues = get_issues()
fpth_save = search_files(df_issues)
