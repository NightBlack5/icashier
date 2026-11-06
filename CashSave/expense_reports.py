import re
import unicodedata
from datetime import date
from html import escape
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def is_expense_pdf_request(message: str) -> bool:
    normalized = unicodedata.normalize("NFKD", message)
    normalized = normalized.encode("ascii", "ignore").decode("ascii").lower()
    return bool(
        re.search(r"\bpdf\b", normalized)
        and re.search(r"\b(gastos?|despesas?)\b", normalized)
    )


def expense_report_data(
    transactions: list[dict],
    categories: list[dict],
) -> tuple[list[dict[str, str | int]], int]:
    category_names = {
        str(category.get("id")): str(category.get("nome") or "Sem categoria")
        for category in categories
    }
    expenses = []
    for transaction in transactions:
        if transaction.get("tipo") != "despesa":
            continue
        category_id = transaction.get("categoria_id")
        expenses.append(
            {
                "data": str(transaction.get("data") or ""),
                "descricao": str(transaction.get("descricao") or "Sem descrição"),
                "categoria": category_names.get(str(category_id), "Sem categoria"),
                "valor_centavos": int(transaction.get("valor_centavos", 0) or 0),
            }
        )
    expenses.sort(key=lambda item: str(item["data"]), reverse=True)
    total = sum(int(item["valor_centavos"]) for item in expenses)
    return expenses, total


def _format_currency(cents: int) -> str:
    value = f"{cents / 100:,.2f}"
    value = value.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {value}"


def generate_expense_pdf(
    transactions: list[dict],
    categories: list[dict],
) -> bytes:
    expenses, total = expense_report_data(transactions, categories)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CashSaveTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=19,
        leading=23,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#047857"),
        spaceAfter=4 * mm,
    )
    meta_style = ParagraphStyle(
        "CashSaveMeta",
        parent=styles["BodyText"],
        fontSize=9,
        textColor=colors.HexColor("#475569"),
        spaceAfter=2 * mm,
    )
    cell_style = ParagraphStyle(
        "CashSaveCell",
        parent=styles["BodyText"],
        fontSize=8,
        leading=10,
    )
    amount_style = ParagraphStyle(
        "CashSaveAmount",
        parent=cell_style,
        alignment=TA_RIGHT,
    )

    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="Relatório de despesas CashSave",
        author="CashSave",
    )
    story = [
        Paragraph("Relatório de despesas", title_style),
        Paragraph(f"Gerado em {date.today().strftime('%d/%m/%Y')}", meta_style),
        Paragraph(f"Lançamentos: {len(expenses)}", meta_style),
        Spacer(1, 4 * mm),
    ]

    rows = [["Data", "Descrição", "Categoria", "Valor"]]
    if expenses:
        for expense in expenses:
            rows.append(
                [
                    Paragraph(escape(str(expense["data"])), cell_style),
                    Paragraph(escape(str(expense["descricao"])), cell_style),
                    Paragraph(escape(str(expense["categoria"])), cell_style),
                    Paragraph(
                        escape(_format_currency(int(expense["valor_centavos"]))),
                        amount_style,
                    ),
                ]
            )
    else:
        rows.append(
            [
                Paragraph("Nenhuma despesa encontrada.", cell_style),
                "",
                "",
                "",
            ]
        )

    table = Table(
        rows,
        colWidths=[24 * mm, 80 * mm, 42 * mm, 34 * mm],
        repeatRows=1,
        hAlign="LEFT",
    )
    table_styles = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111827")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LINEBELOW", (0, 1), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
    ]
    if not expenses:
        table_styles.append(("SPAN", (0, 1), (-1, 1)))
    table.setStyle(TableStyle(table_styles))
    story.append(table)
    story.append(Spacer(1, 5 * mm))

    total_style = ParagraphStyle(
        "CashSaveTotal",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=11,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#047857"),
    )
    total_table = Table(
        [[Paragraph("Total de despesas", styles["BodyText"]), Paragraph(escape(_format_currency(total)), total_style)]],
        colWidths=[120 * mm, 60 * mm],
    )
    total_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    story.append(total_table)
    document.build(story)
    return buffer.getvalue()