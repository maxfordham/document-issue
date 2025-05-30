# document-issue-data

WIP. for now just for collating document-issue-data from excel DNGs.
go to DigitalDesign > Data > document_issue for data and SECRETS scripts.
Copy the scripts in `SECRETS` folder into the gitignored `SECRETS` folder in the root.
Run the following `pixi` tasks, from the project ROOT folder, in the order shown to update the data.

```bash
# execute line by line in the root of the project
# -------------------------
pixi run chmod-scripts
pixi run mnt-jdrive
pixi run get-data  # gets raw doc issue data
pixi run pull-data  # get previously found data
pixi run find-files
pixi run find-latest-add-descriptions # find latest files and add descriptions
pixi run push-data  # push found files back to jobs folder
pixi run cp-to-dashboard  # copy data to dashboard directory

# view the dashboard
pixi run dashboard-install # if not already installed
pixi run dashboard-preview
```
