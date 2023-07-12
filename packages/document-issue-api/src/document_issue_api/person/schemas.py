from document_issue.person import Person  # , Document, Project, Role


class PersonPost(Person):
    pass


class PersonPatch(PersonPost):
    pass


class PersonGet(PersonPost):
    id: int
