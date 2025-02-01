import pathlib
import pandas as pd
import glob

FDIR = pathlib.Path("~/document-issue-data").expanduser()
FDIR_JDRIVE = pathlib.Path("~/jobs").expanduser()
FOUND_FILES_PATH = pathlib.Path("~/found_files_v1.txt").expanduser()

def get_docs():
    # Find all document.csv files
    csv_files = glob.glob(f"{FDIR}/**/document.csv", recursive=True)

    # Initialize an empty list to store dataframes
    dataframes = []

    for file in csv_files:
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

def load_found_files():
    if FOUND_FILES_PATH.exists():
        with open(FOUND_FILES_PATH, 'r') as file:
            lines = file.read().splitlines()
            return {(line.split(',', 2)[0], line.split(',', 2)[1]): line.split(',', 2)[2] for line in lines}
    else:
        return {}

def save_found_files(found_files):
    with open(FOUND_FILES_PATH, 'w') as file:
        for (document_code, date), file_path in found_files.items():
            file.write(f"{document_code},{date},{file_path}\n")

def search_files(df_issues):
    # Load already found files
    found_files_dict = load_found_files()

    # Get unique combinations of project numbers, document codes, and dates
    unique_combinations = df_issues[['project_number', 'document_code', 'date']].drop_duplicates()

    # Initialize a list to store found files
    found_files = []

    for _, row in unique_combinations.iterrows():
        project_number = row['project_number']
        document_code = row['document_code']
        date = row['date']
        
        # Skip if document_code and date are already found
        if (document_code, date) in found_files_dict:
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
            found_files.extend(files)
            if files:
                for file in files:
                    found_files_dict[(document_code, date)] = file
                file_found = True
                break
        
        if not file_found:
            found_files_dict[(document_code, date)] = ""
        
        # Save found files after every found file or not found
        save_found_files(found_files_dict)
    
    return found_files

# Example usage
df_issues = get_issues()
found_files = search_files(df_issues)
print(found_files)