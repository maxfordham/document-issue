import stringcase
import pathlib
import json
import subprocess
from pydantic import ConfigDict, BaseModel, Field, validator
from document_issue.utils import get_stem


def to_sentence(string: str) -> str:
    return stringcase.sentencecase(string).lower()


class BaseModel(BaseModel):
    def file(self, path: pathlib.Path, **json_kwargs):
        if "indent" not in json_kwargs.keys():
            json_kwargs.update({"indent": 4})
        path.write_text(self.model_dump_json(**json_kwargs), encoding="utf-8")

    def file_schema(self, path: pathlib.Path, **json_kwargs):
        path = path.parent / (get_stem(path) + ".schema.json")
        if "indent" not in json_kwargs.keys():
            json_kwargs.update({"indent": 4})
        path.write_text(json.dumps(self.model_json_schema(), **json_kwargs))
        return path

    def file_mdschema(self, path: pathlib.Path, **json_kwargs):
        path_mdschema = path.with_suffix(".md")
        path_schema = self.file_schema(path, **json_kwargs)
        subprocess.run(["jsonschema2md", str(path_schema), str(path_mdschema)])

    model_config = ConfigDict(
        alias_generator=stringcase.snakecase,
        populate_by_name=True,
        from_attributes=True,
        use_enum_values=True,
    )
