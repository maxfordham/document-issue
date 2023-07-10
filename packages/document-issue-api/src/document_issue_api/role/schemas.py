from document_issue.role import Role  # , Document, Project, Role


class RolePost(Role):
    """Role post schema."""

    is_archived: bool = False

    class Config:
        orm_mode = True


class RoleGet(RolePost):
    """Role get schema."""

    id: int
