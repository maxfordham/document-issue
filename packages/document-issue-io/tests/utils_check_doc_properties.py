import pathlib

import yaml
from pypdf import PdfReader

DOCUMENT_PROPERTIES = [
    # "title", # TODO: make issue on quarto describing this...
    # "project", # TODO: make issue on quarto describing this...
    # "subtitle", # TODO: make issue on quarto describing this...
    "author",
    # "subject", # TODO: add to templater.jinja with high-level discipline when available (e.g. mechanical, electrical etc.)
    # "keywords"
]


def get_md_metadata(fpth: pathlib.Path):
    lines = fpth.read_text().split("\n")
    x, y = [n for n, x in enumerate(lines) if x == "---"]
    return yaml.safe_load("\n".join(lines[x + 1 : y - 1]))


def check_quarto_doc_properties(fpth_in: pathlib.Path, fpth_out: pathlib.Path):
    meta_in = get_md_metadata(fpth_in)
    if "author" in meta_in:
        meta_in["author"] = "; ".join(meta_in["author"])
    reader = PdfReader(str(fpth_out))
    meta_out = reader.metadata

    li_get = DOCUMENT_PROPERTIES

    doc_properties_out = []
    for k, v in meta_in.items():
        if k in li_get:
            assert getattr(meta_out, k) == v
            doc_properties_out.append(k)

    if "keywords" in meta_in:
        assert meta_in["keywords"] == meta_out["/Keywords"]
        doc_properties_out.append("keywords")

    return doc_properties_out
