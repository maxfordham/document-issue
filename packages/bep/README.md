# BEP (BIM Execution Plan)

Reference: [BEP](https://www.designingbuildings.co.uk/wiki/BIM_execution_plan_BEP)

Package for storing / retrieving / handling (/visualising?) data standards described in the BIM execution plan.

## Environment Variables

- `BEP_PROJECT_ROLES`: for retrieving the project roles.
  - at MXF we use `BEP_PROJECT_ROLES=mfdb.get_project_roles` to retrieve the internally defined project roles from the database.
  - `mfdb.get_project_roles` is a zero-argument function that returns a dictionary of project roles.