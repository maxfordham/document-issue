from pydantic import ConfigDict, BaseModel, Field, validator
import stringcase
import pathlib
import subprocess
from document_issue.utils import get_stem


def to_sentence(string: str) -> str:
    return stringcase.sentencecase(string).lower()


class BaseModel(BaseModel):
    def file(self, path: pathlib.Path, **json_kwargs):
        if "indent" not in json_kwargs.keys():
            json_kwargs.update({"indent": 4})
        path.write_text(self.json(**json_kwargs), encoding="utf-8")

    def file_schema(self, path: pathlib.Path, **json_kwargs):  # TODO: check this. not sure its working
        path = path.parent / (get_stem(path) + ".schema.json")  # path.with_suffix('.schema.json')
        if "indent" not in json_kwargs.keys():
            json_kwargs.update({"indent": 4})
        path.write_text(self.schema_json(**json_kwargs))  # , encoding='utf-8'
        return path

    def file_mdschema(self, path: pathlib.Path, **json_kwargs):  # TODO: check this. not sure its working
        path_mdschema = path.with_suffix(".md")
        path_schema = self.file_schema(path, **json_kwargs)
        subprocess.run(["jsonschema2md", str(path_schema), str(path_mdschema)])
    model_config = ConfigDict(alias_generator=stringcase.snakecase, populate_by_name=True, from_attributes=True, use_enum_values=True)
