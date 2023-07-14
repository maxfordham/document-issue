from document_issue.role import Role  # , Document, Project, Role


class RolePost(Role):
    """Role post schema."""

    is_archived: bool = False


class RoleGet(RolePost):
    """Role get schema."""

    id: int


class RolePatch(RolePost):
    """Role patch schema."""

    pass
