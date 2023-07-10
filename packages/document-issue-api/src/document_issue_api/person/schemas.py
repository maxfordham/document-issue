from document_issue.person import Person  # , Document, Project, Role


class PersonPost(Person):
    """Role post schema."""

    class Config:
        orm_mode = True


class PersonGet(PersonPost):
    """Role get schema."""

    id: int
