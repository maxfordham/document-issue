import PIL
import pathlib
from datetime import datetime
from textwrap import wrap
from reportlab.lib import colors
from reportlab.lib.units import mm, inch
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, Image, TableStyle, SimpleDocTemplate, TopPadder
from reportlab.pdfgen import canvas

from document_issue.document_issue import DocumentIssue

FDIR_MEDIA = pathlib.Path(__file__).parent / "media"

# Register Callibri fonts
FDIR_FONTS = pathlib.Path(__file__).parent / "fonts"
TTFFILE = FDIR_FONTS / "calibri.ttf"
pdfmetrics.registerFont(TTFont("Calibri", TTFFILE))
TTFFILE = FDIR_FONTS / "calibrib.ttf"  # Bold
pdfmetrics.registerFont(TTFont("Calibri-Bold", TTFFILE))
TTFFILE = FDIR_FONTS / "calibrili.ttf"  # Light Italics
pdfmetrics.registerFont(TTFont("Calibri-Light-Italics", TTFFILE))
TTFFILE = FDIR_FONTS / "calibrii.ttf"  # Italics
pdfmetrics.registerFont(TTFont("Calibri-Italics", TTFFILE))
TTFFILE = FDIR_FONTS / "calibril.ttf"  # Light
pdfmetrics.registerFont(TTFont("Calibri-Light", TTFFILE))
TTFFILE = FDIR_FONTS / "calibrib.ttf"  # Bold Italics
pdfmetrics.registerFont(TTFont("Calibri-Bold-Italics", TTFFILE))


def create_styling(number_of_cols: int) -> list:
    """Create Max Fordham styling for ReportLab table."""
    style = [
        ("BACKGROUND", (0, 0), (1, -1), colors.black),
        ("BACKGROUND", (2, 0), (-1, -1), colors.white),
        ("VALIGN", (0, 0), (0, -1), "MIDDLE"),
        ("LINEABOVE", (0, 0), (-1, 0), 3, colors.black),
        ("LINEBELOW", (0, -1), (-1, -1), 3, colors.black),
        ("LINEBEFORE", (0, 0), (0, -1), 3, colors.black),
        ("SPAN", (0, 0), (1, -1)),  # Span image
        ("SPAN", (7, 1), (-1, 3)),  # Span document title
    ]
    for i in range(number_of_cols):
        if i % 2 == 0:
            style.append(("FONT", (0, i), (-1, i), "Calibri", 7))
            style.append(("TEXTCOLOR", (0, i), (-1, i), colors.gray))
            style.append(("VALIGN", (1, i), (-1, i), "BOTTOM"))
            style.append(("BOTTOMPADDING", (0, i), (-1, i), 0))
        else:
            style.append(("FONT", (0, i), (-1, i), "Calibri-Bold", 12))
            style.append(("TEXTCOLOR", (0, i), (-1, i), colors.black))
            style.append(("VALIGN", (1, i), (-1, i), "TOP"))
            style.append(("TOPPADDING", (0, i), (-1, i), 0))
    return style


def get_title_block_image(fpth_img: pathlib.Path) -> Image:
    """Get the image that will be used within the title block."""
    image = Image(fpth_img)
    image.drawHeight = 28 * mm * image.drawHeight / image.drawWidth
    image.drawWidth = 28 * mm
    return image


def construct_title_block_data(
    document_issue: DocumentIssue,
) -> list[list]:
    """Using the document issue, layout the data in preparation to be styled
    correctly by ReportLab."""
    FPTH_MF_CIRCLE_IMG = FDIR_MEDIA / "mf-circle.png"
    image = get_title_block_image(fpth_img=FPTH_MF_CIRCLE_IMG)
    issue_date = document_issue.current_issue.date.strftime("%d/%m/%Y")
    document_description = "\n".join(wrap(document_issue.document_description, 45))
    name_nomenclature = document_issue.name_nomenclature.replace("-", " - ")
    document_code = document_issue.document_code.replace("-", " - ")
    data = [
        [image, "", "project", "", "", "", "", "document description", "", "", "", ""],
        [
            "",
            "",
            document_issue.project_name,
            "",
            "",
            "",
            "",
            document_description,
            "",
            "",
            "",
            "",
        ],
        [
            "",
            "",
            "job number",
            "director",
            "issue date",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ],
        [
            "",
            "",
            document_issue.project_number,
            document_issue.director_in_charge,
            issue_date,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ],
        [
            "",
            "",
            "status code",
            "revision",
            "status description",
            "",
            "",
            name_nomenclature,
            "",
            "",
            "",
            "",
        ],
        [
            "",
            "",
            document_issue.current_issue.status_code,
            document_issue.current_issue.revision,
            document_issue.current_issue.status_description,
            "",
            "",
            document_code,
            "",
            "",
            "",
            "",
        ],
    ]
    return data


def create_title_block_table(data: list):
    """Create the ReportLab table and set the styling."""
    table = Table(data, colWidths="*")
    styling = create_styling(len(data))
    table.setStyle(TableStyle(styling))
    return table


def build_title_block_pdf(
    document_issue: DocumentIssue,
    fpth_output: pathlib.Path = pathlib.Path("title-block.pdf"),
):
    """Build a PDF with just the Max Fordham title block at the bottom of an
    A4 page."""
    data = construct_title_block_data(document_issue=document_issue)
    title_block_table = create_title_block_table(data=data)
    doc = SimpleDocTemplate(
        str(fpth_output),
        pagesize=A4,
        leftMargin=0.25 * inch,
        rightMargin=0.25 * inch,
        bottomMargin=0.5 * inch,
        topMargin=inch,
    )
    elements = [TopPadder(title_block_table)]
    doc.build(elements)


def set_background(canvas: canvas, doc: SimpleDocTemplate):
    """Create function that will set the Max Fordham background."""
    FPTH_MF_TITLE = FDIR_MEDIA / "mf-title.png"
    image = PIL.Image.open(FPTH_MF_TITLE)
    mf_title_width, mf_title_height = image.size

    FPTH_MF_BACKGROUND = FDIR_MEDIA / "mf-background.png"
    image = PIL.Image.open(FPTH_MF_BACKGROUND)
    mf_background_width, mf_background_height = image.size
    a4_image_ratio = A4[1] / mf_background_height
    canvas.saveState()
    canvas.drawImage(
        FPTH_MF_BACKGROUND,
        x=170,
        y=0,
        width=mf_background_width * a4_image_ratio,
        height=A4[1],
    )
    canvas.drawImage(
        FPTH_MF_TITLE,
        x=535,
        y=510,
        width=0.35 * mf_title_width,
        height=0.35 * mf_title_height,
        mask="auto",
    )
    canvas.restoreState()


def build_schedule_title_page_template_pdf(
    document_issue: DocumentIssue,
    fpth_output: pathlib.Path = pathlib.Path("title-page.pdf"),
):
    """Build a PDF with a title block and the Max Fordham background."""
    data = construct_title_block_data(document_issue=document_issue)
    title_block_table = create_title_block_table(data=data)
    doc = SimpleDocTemplate(
        str(fpth_output),
        pagesize=A4,
        leftMargin=0.25 * inch,
        rightMargin=0.25 * inch,
        bottomMargin=0.5 * inch,
        topMargin=inch,
    )
    elements = [TopPadder(title_block_table)]
    doc.build(elements, onFirstPage=set_background)
