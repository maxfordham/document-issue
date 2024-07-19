import PIL
import pathlib
from textwrap import wrap
from reportlab.lib import colors
from reportlab.lib.units import mm, inch
from reportlab.lib.pagesizes import A4, A3, landscape
from reportlab.platypus import Table, Image, TableStyle, SimpleDocTemplate, TopPadder
from reportlab.pdfgen import canvas

from document_issue.document_issue import DocumentIssue
from .constants import MAP_TITLEBLOCK_IMAGES, FPTH_MF_CIRCLE_IMG, DIR_MEDIA
from .styles import register_fonts

register_fonts()


def titleblockimage(loc):
    return MAP_TITLEBLOCK_IMAGES[loc.lower()]


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


def get_title_block_image(
    fpth_img: pathlib.Path, scale_height=28, scale_width=28
) -> Image:
    """Get the image that will be used within the title block."""

    image = Image(fpth_img)
    image.drawHeight = scale_height * mm * image.drawHeight / image.drawWidth
    image.drawWidth = scale_width * mm
    return image


def construct_title_block_data(
    document_issue: DocumentIssue,
    fpth_img=FPTH_MF_CIRCLE_IMG,
    scale_height=28,
    scale_width=28,
    is_a3=False,
) -> list[list]:
    """Using the document issue, layout the data in preparation to be styled
    correctly by ReportLab."""

    image = get_title_block_image(
        fpth_img=fpth_img, scale_height=scale_height, scale_width=scale_width
    )
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
            "project number",
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
            document_issue.current_issue.status_description.replace(
                "Suitable for ", ""
            ).replace(
                "Issued for ", ""
            ),  # TODO: Need to deal with length of status codes more robustly
            "",
            "",
            document_code,
            "",
            "",
            "",
            "",
        ],
    ]
    if is_a3:
        data[0][4] = "client"
        data[1][4] = document_issue.client_name
    # data = [d[0:-3] for d in data]
    # data = [d[0:5] + d[7:] for d in data]
    return data


def create_title_block_table(data: list, is_a3=False) -> Table:
    """Create the ReportLab table and set the styling."""
    if is_a3:
        table = Table(data, colWidths=[180] + ["*"] * 5)
    else:
        table = Table(data, colWidths="*")
    styling = create_styling(len(data))
    table.setStyle(TableStyle(styling))
    return table


def set_background(canvas: canvas, doc: SimpleDocTemplate):
    """Create function that will set the Max Fordham background."""
    FPTH_MF_TITLE = DIR_MEDIA / "mf-title.png"
    image = PIL.Image.open(FPTH_MF_TITLE)
    mf_title_width, mf_title_height = image.size

    FPTH_MF_BACKGROUND = DIR_MEDIA / "mf-background.png"
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


def title_block_table(
    document_issue: DocumentIssue,
    is_a3: bool = False,
    office: str = "london",
):
    if is_a3:
        fpth_img = titleblockimage(office)
        scale_height = 88
        scale_width = 88
    else:
        fpth_img = FPTH_MF_CIRCLE_IMG
        scale_height = 28
        scale_width = 28
    data = construct_title_block_data(
        document_issue=document_issue,
        fpth_img=fpth_img,
        is_a3=is_a3,
        scale_height=scale_height,
        scale_width=scale_width,
    )
    return create_title_block_table(data=data, is_a3=is_a3)


def title_block_a4(
    document_issue: DocumentIssue,
    fpth_output: pathlib.Path = pathlib.Path("title-page.pdf"),
    is_titlepage: bool = False,
):
    tblock_table = title_block_table(document_issue=document_issue, is_a3=False)
    doc = SimpleDocTemplate(
        str(fpth_output),
        pagesize=A4,
        leftMargin=0.25 * inch,
        rightMargin=0.25 * inch,
        bottomMargin=0.5 * inch,
        topMargin=inch,
    )
    elements = [TopPadder(tblock_table)]
    if is_titlepage:
        doc.build(elements, onFirstPage=set_background)
    else:
        doc.build(elements)


def title_block_a3(
    document_issue: DocumentIssue,
    fpth_output: pathlib.Path = pathlib.Path("title-block-a3.pdf"),
    is_titlepage: bool = False,
):
    tblock_table = title_block_table(document_issue=document_issue, is_a3=True)
    doc = SimpleDocTemplate(
        str(fpth_output),
        pagesize=landscape(A3),
        leftMargin=0.25 * inch,
        rightMargin=0.25 * inch,
        bottomMargin=0.5 * inch,
        topMargin=inch,
    )
    elements = [TopPadder(tblock_table)]
    if is_titlepage:
        doc.build(elements, onFirstPage=set_background)
    else:
        doc.build(elements)


def build_schedule_title_page_template_pdf(
    document_issue: DocumentIssue,
    fpth_output: pathlib.Path = pathlib.Path("title-page.pdf"),
):
    """Build a PDF with a title block and the Max Fordham background."""
    title_block_a4(
        document_issue=document_issue, fpth_output=fpth_output, is_titlepage=True
    )
