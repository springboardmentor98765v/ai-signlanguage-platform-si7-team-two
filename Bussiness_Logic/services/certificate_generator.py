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

def generate_certificate_pdf(
    learner_name: str,
    average_score: float,
    certificate_code: str,
) -> str:

    os.makedirs(CERTIFICATES_DIR, exist_ok=True)

    filename = f"{certificate_code}.pdf"
    file_path = os.path.join(CERTIFICATES_DIR, filename)

    width, height = landscape(A4)

    c = canvas.Canvas(file_path, pagesize=landscape(A4))

    # =====================================================
    # Double Border
    # =====================================================
    c.setStrokeColor(colors.darkblue)
    c.setLineWidth(4)
    c.rect(1 * cm, 1 * cm, width - 2 * cm, height - 2 * cm)

    c.setStrokeColor(colors.gold)
    c.setLineWidth(1.5)
    c.rect(1.4 * cm, 1.4 * cm, width - 2.8 * cm, height - 2.8 * cm)

    # =====================================================
    # Platform Name
    # =====================================================
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(
        width / 2,
        height - 2.5 * cm,
        "AI SIGN LANGUAGE LEARNING PLATFORM"
    )

    # =====================================================
    # Certificate Title
    # =====================================================
    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(colors.HexColor("#B8860B"))
    c.drawCentredString(
        width / 2,
        height - 4.5 * cm,
        "CERTIFICATE OF COMPLETION"
    )

    # =====================================================
    # Award Text
    # =====================================================
    c.setFont("Helvetica", 16)
    c.setFillColor(colors.black)
    c.drawCentredString(
        width / 2,
        height - 6.5 * cm,
        "This certificate is proudly presented to"
    )

    # =====================================================
    # Learner Name
    # =====================================================
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(
        width / 2,
        height - 8.5 * cm,
        learner_name.upper()
    )

    # =====================================================
    # Achievement
    # =====================================================
    c.setFont("Helvetica", 15)

    c.drawCentredString(
        width / 2,
        height - 10.2 * cm,
        "for successfully completing the"
    )

    c.drawCentredString(
        width / 2,
        height - 11.0 * cm,
        "AI Sign Language Learning Course"
    )

    c.drawCentredString(
        width / 2,
        height - 11.8 * cm,
        f"with an average accuracy of {average_score:.2f}%"
    )

    # =====================================================
    # Decorative Line
    # =====================================================
    c.setStrokeColor(colors.grey)
    c.line(4 * cm, height - 13.2 * cm, width - 4 * cm, height - 13.2 * cm)

    # =====================================================
    # Date
    # =====================================================
    today = datetime.utcnow().strftime("%d %B %Y")

    c.setFont("Helvetica", 12)

    c.drawString(
        2.5 * cm,
        2.8 * cm,
        f"Issue Date: {today}"
    )

    # =====================================================
    # Certificate Code
    # =====================================================
    c.drawRightString(
        width - 2.5 * cm,
        2.8 * cm,
        f"Certificate ID: {certificate_code}"
    )

    # =====================================================
    # Signature
    # =====================================================
    c.line(
        width / 2 - 3 * cm,
        3.8 * cm,
        width / 2 + 3 * cm,
        3.8 * cm,
    )

    c.setFont("Helvetica", 12)

    c.drawCentredString(
        width / 2,
        3.1 * cm,
        "Course Instructor"
    )

    # =====================================================
    # Verification Seal
    # =====================================================
    c.setFont("Helvetica-Bold", 13)

    c.setFillColor(colors.darkgreen)

    c.drawCentredString(
        width / 2,
        2.1 * cm,
        "✓ VERIFIED CERTIFICATE"
    )

    c.save()

    return file_path