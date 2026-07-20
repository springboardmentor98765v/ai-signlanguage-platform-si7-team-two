"""
Certificate PDF Generator — Milestone 2, Day 7.

Generates a simple, clean certificate PDF using ReportLab, showing the
learner's name, date, and achievement (average score). Kept intentionally
simple (text + basic design, no complex graphics) per SRS risk mitigation
note (Section 10: "keep the design simple... no complex graphics").
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas

CERTIFICATES_DIR = "generated_certificates"


def generate_certificate_pdf(learner_name: str, average_score: float, certificate_code: str) -> str:
    """
    Generates a certificate PDF and returns the file path.
    """
    os.makedirs(CERTIFICATES_DIR, exist_ok=True)

    filename = f"{certificate_code}.pdf"
    file_path = os.path.join(CERTIFICATES_DIR, filename)

    page_width, page_height = landscape(A4)
    c = canvas.Canvas(file_path, pagesize=landscape(A4))

    # Border
    c.setStrokeColor(colors.HexColor("#2C3E50"))
    c.setLineWidth(4)
    c.rect(1 * cm, 1 * cm, page_width - 2 * cm, page_height - 2 * cm)

    # Title
    c.setFont("Helvetica-Bold", 32)
    c.setFillColor(colors.HexColor("#2C3E50"))
    c.drawCentredString(page_width / 2, page_height - 4 * cm, "Certificate of Achievement")

    # Subtitle
    c.setFont("Helvetica", 16)
    c.setFillColor(colors.black)
    c.drawCentredString(page_width / 2, page_height - 5.5 * cm, "Sign Language Learning & Assessment Platform")

    # "This certifies that"
    c.setFont("Helvetica", 14)
    c.drawCentredString(page_width / 2, page_height - 8 * cm, "This certifies that")

    # Learner name
    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(colors.HexColor("#1A5276"))
    c.drawCentredString(page_width / 2, page_height - 9.5 * cm, learner_name)

    # Achievement text
    c.setFont("Helvetica", 14)
    c.setFillColor(colors.black)
    c.drawCentredString(
        page_width / 2,
        page_height - 11.5 * cm,
        f"has successfully completed the Alphabet Sign Language course"
    )
    c.drawCentredString(
        page_width / 2,
        page_height - 12.5 * cm,
        f"with an average accuracy of {average_score}%"
    )

    # Date
    today_str = datetime.utcnow().strftime("%B %d, %Y")
    c.setFont("Helvetica", 12)
    c.drawString(2.5 * cm, 2.5 * cm, f"Date: {today_str}")

    # Certificate code (bottom right, for verification)
    c.drawRightString(page_width - 2.5 * cm, 2.5 * cm, f"Certificate ID: {certificate_code}")

    c.save()
    return file_path