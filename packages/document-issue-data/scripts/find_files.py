import pathlib
import pandas as pd
import glob
from datetime import datetime

def datetime_string(): return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

FDIR = pathlib.Path(__file__).parent / "data-raw" / "config"
FDIR_JDRIVE = pathlib.Path("~/jobs").expanduser()
FDIR_FIND_FILES = pathlib.Path(__file__).parent / "data-processed"
FPTH_MESSAGE = pathlib.Path(__file__).parent / "findfiles-message.txt"

def get_docs():
    # Find all document.csv files
    csv_files = glob.glob(f"{FDIR}/**/document.csv", recursive=True)

    # Initialize an empty list to store dataframes
    dataframes = []

    for file in csv_files[0:2]:
        # Extract the project number from the directory path
        project_number = int(pathlib.Path(file).parts[-2].replace("J", ""))
        
        # Load the data from the document.csv file
        df = pd.read_csv(file)
        
        # Add a column for the project number
        df['project_number'] = project_number
        
        # Append the dataframe to the list
        dataframes.append(df)

    # Concatenate all dataframes into a single dataframe
    return pd.concat(dataframes, ignore_index=True)

def get_issues():
    # Find all issue.csv files
    csv_files = glob.glob(f"{FDIR}/**/issue.csv", recursive=True)

    # Initialize an empty list to store dataframes
    dataframes = []

    for file in csv_files:
        # Extract the project number from the directory path
        project_number = int(pathlib.Path(file).parts[-2].replace("J", ""))
        
        # Load the data from the issue.csv file
        df = pd.read_csv(file)
        
        # Add a column for the project number
        df['project_number'] = project_number
        
        # Split the date_status column into date and status columns
        df[['date', 'status']] = df['date_status'].str.split('-', expand=True)
        
        # Drop the original date_status column
        df.drop(columns=['date_status'], inplace=True)
        
        # Append the dataframe to the list
        dataframes.append(df)

    # Concatenate all dataframes into a single dataframe
    df_issues = pd.concat(dataframes, ignore_index=True)
    
    return df_issues





def get_found_files():
    return list(FDIR_FIND_FILES.glob("found_files*.txt"))

def load_found_files(fpths):
    
    found = {}
    missing = {}
    for fpth in fpths:
        with open(fpth, 'r') as file:
            lines = file.read().splitlines()
            _ = {(line.split(',', 2)[0], line.split(',', 2)[1]): line.split(',', 2)[2] for line in lines}
            found = found | {k:v for k, v in _.items() if v != "" }
            missing = missing | {k:v for k, v in _.items() if v == "" }

    for x in list(missing.keys()):
        if x in found.keys():
            missing.pop(x)

    return found, missing

def save_found_files(found_files, fpth):
    with open(fpth, 'w') as file:
        for (document_code, date), file_path in found_files.items():
            file.write(f"{document_code},{date},{file_path}\n")

def search_files(df_issues, ignore_missing=True):
    fpths = get_found_files()
    # Load already found files
    found, missing = load_found_files(fpths)
    fpth_save = FDIR_FIND_FILES / f"found_files_{str(len(list(fpths))+1)}.txt"
    found_files_dict = {} # found within this session
    
    # Get unique combinations of project numbers, document codes, and dates
    unique_combinations = df_issues[['project_number', 'document_code', 'date']].drop_duplicates()


    for _, row in unique_combinations.iterrows():
        project_number = row['project_number']
        document_code = row['document_code']
        if "\n" in document_code:
            document_code = document_code.replace("\n", "")
        date = row['date']
        
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


