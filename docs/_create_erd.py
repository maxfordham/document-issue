import os
import pathlib
import sys
import erdantic as erd

DIR_MODULE = pathlib.Path(__file__).parents[1] / "src"
DIR_OUT = pathlib.Path(__file__).parent / "images"
sys.path.append(str(DIR_MODULE))

from document_issue.document import DocumentIssue

erd.draw(
    DocumentIssue,
    out=DIR_OUT / "erd-{}.png".format(DocumentIssue.__name__),
)
