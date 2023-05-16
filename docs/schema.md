# Document Issue Schema


*metadata to be accompanied by every formal document issue.

Not all data fields are required for every document type,
but no document will require additional data fields.*

## Properties

- **`project_name`** *(string)*: should be the same as the WebApp. Default: `In House App Testing`.
- **`project_number`** *(string)*: unique number project code. Default: `J5001`.
- **`roles`** *(array)*: defines who is fulfilling various roles and responsibilitieson the project. Some of these roles are required from a QA and quality assurance perspective. Default: `[{'name': 'JG', 'role': 'Project Engineer'}]`.
  - **Items**: Refer to *#/definitions/Role*.
- **`document_name`** *(string)*: document code. Should be the filename when uploadedto a CDE. Structured to be machine-readable. Default: `06667-MXF-XX-XX-SH-M-20003`.
- **`document_description`** *(string)*: human readable description of the document. Default: `Document Description`.
- **`classification`** *(string)*: classification as per Uniclass2015. Default: `Ac_05`.
- **`name_nomenclature`** *(string)*: denotes what each section of of the document code meanswhen split on '-' character. Default: `project-originator-volume-level-type-role-number`.
- **`size`** *(string)*: paper size of the document. Default: `A4`.

  Examples:
  ```json
  "n/a"
  ```

  ```json
  "A4"
  ```

  ```json
  "A3"
  ```

  ```json
  "A2"
  ```

  ```json
  "A1"
  ```

  ```json
  "A0"
  ```

- **`scale`** *(string)*: if drawing, give scale, else "not to scale" (NTS). Default: `NTS`.

  Examples:
  ```json
  "nts"
  ```

  ```json
  "1:1"
  ```

  ```json
  "1:2"
  ```

  ```json
  "1:5"
  ```

  ```json
  "1:10"
  ```

  ```json
  "1:20"
  ```

  ```json
  "1:25"
  ```

  ```json
  "1:50"
  ```

  ```json
  "1:100"
  ```

  ```json
  "1:200"
  ```

  ```json
  "1:250"
  ```

  ```json
  "1:500"
  ```

  ```json
  "1:1000"
  ```

  ```json
  "1:1250"
  ```

- **`doc_source`** *(string)*: software used to author the document. Default: `WD`.

  Examples:
  ```json
  "A"
  ```

  ```json
  "R18"
  ```

  ```json
  "R19"
  ```

  ```json
  "R20"
  ```

  ```json
  "R21"
  ```

  ```json
  "R22"
  ```

  ```json
  "R23"
  ```

  ```json
  "PDF"
  ```

  ```json
  "PSD"
  ```

  ```json
  "PNG"
  ```

  ```json
  "WD"
  ```

  ```json
  "EXL"
  ```

  ```json
  "AM"
  ```

- **`issue_history`** *(array)*: Default: `[{'revision': 'P01', 'date': '2020-01-02', 'status_code': 'S2', 'status_description': 'Suitable for information', 'author': 'EG', 'checked_by': 'CK', 'issue_format': 'cde', 'issue_notes': ''}]`.
  - **Items**: Refer to *#/definitions/Issue*.
- **`notes`** *(array)*: Default: `['add notes here']`.
  - **Items** *(string)*
- **`originator`** *(string)*: the company the info came from (fixed to be Max Fordham LLP). the name 'originator' comes from BS EN ISO 19650-2. Default: `Max Fordham LLP`.
- **`format_configuration`**: Default: `{'date_string_format': '%d %^b %y', 'include_author_and_checked_by': False}`.
## Definitions

- **`Role`** *(object)*
  - **`name`** *(string)*: initial of the person fulfilling the Role. Default: `JG`.
  - **`role`** *(string)*: Default: `Project Engineer`.

    Examples:
    ```json
    ""
    ```

    ```json
    "Director in Charge"
    ```

    ```json
    "Client Relationship Management (CRM) Lead"
    ```

    ```json
    "Management Lead"
    ```

    ```json
    "Commercial Lead"
    ```

    ```json
    "Design Strategy Lead"
    ```

    ```json
    "Health and Safety Lead"
    ```

    ```json
    "Project Coordinator"
    ```

    ```json
    "Project Administrator"
    ```

    ```json
    "Strategy Reviewer"
    ```

    ```json
    "Technical Reviewer"
    ```

    ```json
    "Project Engineer"
    ```

    ```json
    "Lead Electrical Engineer"
    ```

    ```json
    "Lead Mechanical Engineer"
    ```

    ```json
    "Systems Engineer"
    ```

    ```json
    "Site Engineer"
    ```

    ```json
    "BIM Strategy Advisor"
    ```

    ```json
    "Digital Design Engineer"
    ```

    ```json
    "Responsible Building Performance Modeller"
    ```

    ```json
    "Building Performance Modeller"
    ```

    ```json
    "Lead Sustainability Consultant"
    ```

    ```json
    "Sustainability Consultant"
    ```

    ```json
    "Lead Acoustician"
    ```

    ```json
    "Specialist Building Physics Engineer"
    ```

    ```json
    "Specialist Lighting Designer"
    ```

    ```json
    "Passivhaus Principal"
    ```

    ```json
    "Passivhaus Project Designer"
    ```

    ```json
    "Passivhaus Designer"
    ```

- **`IssueFormatEnum`** *(string)*: in what form was the issue delivered. Must be one of: `['cde', 'ea', 'el', 'p', 'r']`.
- **`Issue`** *(object)*: required information fields that define the metadata of a document issue.
  - **`revision`** *(string)*: Default: `P01`.
  - **`date`** *(string)*: Default: `2020-01-02`.
  - **`status_code`** *(string)*: Default: `S2`.
  - **`status_description`** *(string)*: this is a BIM field that matches directly with status_code. Default: `Suitable for information`.
  - **`author`** *(string)*: the person who authored the work. Default: `EG`.
  - **`checked_by`** *(string)*: the person who checked the work. . Default: `CK`.
  - **`issue_format`**: Default: `cde`.
  - **`issue_notes`** *(string)*: free field where the Engineer can briefly summarise changes since previous issue. Default: ``.
- **`FormatConfiguration`** *(object)*: configuration options that determine how the output is displayed.
  - **`date_string_format`** *(string)*: date display format. refer to: https://www.programiz.com/python-programming/datetime/strptime. Default: `%d %^b %y`.
  - **`include_author_and_checked_by`** *(boolean)*: Include the initials of the author and checker in the client facing output. Often avoided but some clients (e.g. Canary Wharf) require it. Default: `False`.
