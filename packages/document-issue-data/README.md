# document-issue-data

WIP. for now just for collating document-issue-data from excel DNGs.
go to DigitalDesign > Data > document_issue for data and SECRETS scripts.
Copy the scripts in `SECRETS` folder into the gitignored `SECRETS` folder in the root.
Run the following `pixi` tasks, from the project ROOT folder, in the order shown to update the data.

```bash
pixi run chmod-scripts
pixi run mnt-jdrive
pixi run get-data  # gets raw doc issue data
pixi run pull-data  # get previously found data
pixi run find-files
pixi run push-data  # push found files back to jobs folder
```
