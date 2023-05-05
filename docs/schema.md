# Document Issue Schema


*metadata to be accompanied by every formal document issue.

__Aspiration__: not all data fields are required for every document type,
but no document will require additional data fields.

__Note__: The parameter names are stored in the background as "snake_case"
but are output as "sentence case" (all lower case). This is configurable and simple to change.*

## Properties

- **`project_name`** *(string)*: Default: `In House App Testing`.
- **`project_number`** *(string)*: Default: `J5001`.
- **`fpth_job_data_ini`** *(string)*: Default: ``.
- **`roles`** *(array)*: defines who is fulfilling various roles on the project.currently the there is no validation on the "allowed roles", but in the future this should probably link up with the work Dan, Andy and Dean having been doing  on roles and responsibilities. It is suggested that the __Project Leader__ (or senior partner...)role should be required on every project, and that only 1no Project Leader can exist on a project at a given time. Any document can then inherit this Project Leader field.[TODO: fix the required roles for a project / integrate with WebApp]{custom-style="mf_green"}.
  - **Items**: Refer to *#/definitions/Role*.
- **`document_name`** *(string)*: Default: `06667-MXF-XX-XX-SH-M-20003`.
- **`document_description`** *(string)*: Default: `Document Description`.
- **`classification`** *(string)*: classification as per Uniclass2015. Default: `Ac_05`.
- **`name_nomenclature`** *(string)*: Default: `project code-originator-volume-level-type-role-number`.
- **`size`** *(string)*: paper size of the document. Default: `A4`.
- **`scale`** *(string)*: if drawing, give scale, else "not to scale" (NTS). Default: `NTS`.
- **`doc_source`** *(string)*: software used to author the document. Default: `WD`.
- **`date_string_format`** *(string)*: Default: `%d %^b %y`.
- **`description_in_filename`** *(boolean)*: Default: `False`.
- **`include_author_and_checked_by`** *(boolean)*: Default: `False`.
- **`issue_history`** *(array)*
  - **Items**: Refer to *#/definitions/Issue*.
- **`notes`** *(array)*
  - **Items** *(string)*
- **`originator`** *(string)*: the company the info came from (fixed to be Max Fordham LLP). the name 'originator' comes from BS EN ISO 19650-2. Default: `Max Fordham LLP`.
- **`format_configuration`**: Default: `{'date_string_format': '%d %^b %y', 'description_in_filename': False, 'include_author_and_checked_by': False}`.
## Definitions

- **`Role`** *(object)*
  - **`name`** *(string)*: initial of the person fulfilling the Role. Default: `JG`.
  - **`role`** *(string)*: Default: `Project Engineer`.
- **`IssueFormatEnum`** *(string)*: An enumeration. Must be one of: `['cde', 'ea', 'el', 'p', 'r']`.
- **`Issue`** *(object)*: required information fields that define the metadata of a document issue.
  - **`revision`** *(string)*: Default: `P01`.
  - **`date`** *(string)*: Default: `2020-01-02`.
  - **`status_code`** *(string)*: Default: `S2`.
  - **`status_description`** *(string)*: this is a BIM field that matches directly with status_code. TODO: add validation. Default: `Suitable for information`.
  - **`author`** *(string)*: 
the person who authored the work. 
this is an optional field as for many info types listing a single author is not appropriate. 
_could change the type to be either a single author or a list of authors..._
this field has been explicitly requested by Canary Wharf. Default: `EG`.
  - **`checked_by`** *(string)*: 
the person who checked the work. 
this is an optional field as for many info types listing a single checked_by is not appropriate. 
_could change the type to be either a single author or a list of authors..._
this field has been explicitly requested by Canary Wharf.
it is most appropriate for drawings - less so for Spec. . Default: `CK`.
  - **`issue_format`**: in what form was the issue delivered. Default: `cde`.
  - **`issue_notes`** *(string)*: free field where the Engineer can briefly summarise changes since previous issue. Default: ``.
- **`FormatConfiguration`** *(object)*
  - **`date_string_format`** *(string)*: Default: `%d %^b %y`.
  - **`description_in_filename`** *(boolean)*: Default: `False`.
  - **`include_author_and_checked_by`** *(boolean)*: Default: `False`.
