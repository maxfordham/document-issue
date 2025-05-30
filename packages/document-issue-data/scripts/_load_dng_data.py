import pathlib
import glob
import pandas as pd

FDIR_RAW = pathlib.Path(__file__).parent / "data-raw"


def get_docs():
    # Find all document.csv files
    csv_files = glob.glob(f"{FDIR_RAW}/**/document.csv", recursive=True)

    # Initialize an empty list to store dataframes
    dataframes = []

    for file in csv_files:
        # Extract the project number from the directory path
        project_number = int(pathlib.Path(file).parts[-2].replace("J", ""))

        # Load the data from the document.csv file
        df = pd.read_csv(file)

        # Add a column for the project number
        df["project_number"] = project_number

        # Append the dataframe to the list
        dataframes.append(df)

    # Concatenate all dataframes into a single dataframe
    return pd.concat(dataframes, ignore_index=True)


def get_issues():
    # Find all issue.csv files
    csv_files = glob.glob(f"{FDIR_RAW}/**/issue.csv", recursive=True)

    # Initialize an empty list to store dataframes
    dataframes = []

    for file in csv_files:
        # Extract the project number from the directory path
        project_number = int(pathlib.Path(file).parts[-2].replace("J", ""))

        # Load the data from the issue.csv file
        df = pd.read_csv(file)

        # Add a column for the project number
        df["project_number"] = project_number

        # Split the date_status column into date and status columns
        df[["date", "status"]] = df["date_status"].str.split("-", expand=True)

        # Drop the original date_status column
        df.drop(columns=["date_status"], inplace=True)

        # Append the dataframe to the list
        dataframes.append(df)
    # Concatenate all dataframes into a single dataframe
    df_issues = pd.concat(dataframes, ignore_index=True)

    return df_issues


if __name__ == "__main__":
    df_docs = get_docs()
    df_issues = get_issues()
    print(df_docs.head())
    print(df_issues.head())
