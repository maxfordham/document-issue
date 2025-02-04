
import pathlib

import yaml
from pypdf import PdfReader

DOCUMENT_PROPERTIES = [
        "title",
        # "project", # TODO: not coming through -> make issue on quarto describing this...
        # "subtitle", # TODO: not coming through -> make issue on quarto describing this...
        "author",
        "subject",
        # "keywords"
    ]


def get_md_metadata(fpth: pathlib.Path):
    lines = fpth.read_text().split("\n")
    x, y = [n for n, x in enumerate(lines) if x == "---"]
    return yaml.safe_load("\n".join(lines[x+1:y-1]))

def check_quarto_doc_properties(fpth_in: pathlib.Path, fpth_out: pathlib.Path):
    meta_in = get_md_metadata(fpth_in)
    if "author" in meta_in:
        meta_in["author"] = "; ".join(meta_in["author"])
    reader = PdfReader(str(fpth_out))
    meta_out = reader.metadata

    li_get = DOCUMENT_PROPERTIES

    for k, v in meta_in.items():
        if k in li_get:
            assert getattr(meta_out, k) == v

    if "keywords" in meta_in:
        assert meta_in["keywords"] == meta_out["/Keywords"]

    return li_get
