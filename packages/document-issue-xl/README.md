# document-issue-xl

Excel file for storing document-issue data and generating issue sheet. 
Issue sheet generation is done by a compiled python program (executable using cx_Freeze).

## Deploying

- python program
  - build the python program based on instructions in `./src/document-issue-xl/README.txt`
  - copy and paste `build` folder to Y:\drive location:
    - `./src/document-issue-xl` -> `Y:\Git_Projects\MF_Toolbox\dev\mf_xlwings\document_issue`
    - rename the folder `exe.win-amd64-3.12` -> `exe.win-amd64-3.6` to ensure old links still work
- excel DNG
  - copy and paste excel template file to Y:\drive location:
    - `./xl/DocumentNumberGenerator.xltm` -> `Y:\Git_Projects\MF_Toolbox\dev\mf_xlwings\document_issue\DocumentNumberGenerator.xltm`

*__note__. Y:\drive directory unchanged for backward compatibility, but the rest of MF_Toolbox repo has been removed.*