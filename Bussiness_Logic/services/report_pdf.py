"""
Report PDF Generator — Milestone 4, Day 4.

Generates PDF reports for:
1. Learning
2. Assessment
3. Accuracy
4. Certification

Uses ReportLab, the same library already used by the
existing certificate and progress report generators.
"""

import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


REPORTS_DIR = "generated_reports"


# ---------------------------------------------------------
# COMMON PDF SETUP
# ---------------------------------------------------------

def _create_pdf(
    filename: str,
    title: str,
    learner_name: str,
):
    """
    Creates a basic PDF canvas with a common header.
    """

    os.makedirs(REPORTS_DIR, exist_ok=True)

    file_path = os.path.join(
        REPORTS_DIR,
        filename,
    )

    page_width, page_height = A4

    c = canvas.Canvas(
        file_path,
        pagesize=A4,
    )

    # Title
    c.setFont(
        "Helvetica-Bold",
        20,
    )

    c.setFillColor(
        colors.HexColor("#2C3E50")
    )

    c.drawCentredString(
        page_width / 2,
        page_height - 2.5 * cm,
        title,
    )

    # Learner name
    c.setFont(
        "Helvetica",
        12,
    )

    c.setFillColor(colors.black)

    c.drawCentredString(
        page_width / 2,
        page_height - 3.5 * cm,
        learner_name or "Learner",
    )

    return c, file_path


def _draw_line(
    c,
    y,
    label,
    value,
):
    """
    Draws one label/value row.
    """

    c.setFont(
        "Helvetica-Bold",
        11,
    )

    c.drawString(
        2.5 * cm,
        y,
        f"{label}:",
    )

    c.setFont(
        "Helvetica",
        11,
    )

    c.drawString(
        8 * cm,
        y,
        str(value),
    )


def _finish_pdf(c, file_path):
    """
    Adds generation date and saves the PDF.
    """

    page_width, _ = A4

    today = datetime.utcnow().strftime(
        "%B %d, %Y"
    )

    c.setFont(
        "Helvetica",
        9,
    )

    c.setFillColor(colors.grey)

    c.drawString(
        2.5 * cm,
        1.5 * cm,
        f"Generated on {today}",
    )

    c.save()

    return file_path


# ---------------------------------------------------------
# 1. LEARNING REPORT PDF
# ---------------------------------------------------------

def generate_learning_report_pdf(
    learner_name: str,
    report_data: dict,
    user_id: str,
) -> str:

    c, file_path = _create_pdf(
        filename=f"Learning_Report_{user_id}.pdf",
        title="Learner Learning Report",
        learner_name=learner_name,
    )

    y = A4[1] - 5 * cm

    _draw_line(
        c,
        y,
        "Total Sessions",
        report_data["total_sessions"],
    )

    y -= 0.8 * cm

    _draw_line(
        c,
        y,
        "Completed Sessions",
        report_data["completed_sessions"],
    )

    y -= 0.8 * cm

    _draw_line(
        c,
        y,
        "Practice Time (sec)",
        report_data["total_practice_time"],
    )

    y -= 0.8 * cm

    _draw_line(
        c,
        y,
        "Total Assessments",
        report_data["total_assessments"],
    )

    y -= 0.8 * cm

    _draw_line(
        c,
        y,
        "Letters Attempted",
        ", ".join(
            report_data["attempted_letters"]
        ) or "None",
    )

    return _finish_pdf(
        c,
        file_path,
    )


# ---------------------------------------------------------
# 2. ASSESSMENT REPORT PDF
# ---------------------------------------------------------

def generate_assessment_report_pdf(
    learner_name: str,
    report_data: dict,
    user_id: str,
) -> str:

    c, file_path = _create_pdf(
        filename=f"Assessment_Report_{user_id}.pdf",
        title="Assessment Report",
        learner_name=learner_name,
    )

    y = A4[1] - 5 * cm

    _draw_line(
        c,
        y,
        "Total Assessments",
        report_data["total_assessments"],
    )

    y -= 0.8 * cm

    _draw_line(
        c,
        y,
        "Average Score",
        f"{report_data['average_score']}%",
    )

    y -= 0.8 * cm

    _draw_line(
        c,
        y,
        "Correct Assessments",
        report_data["correct_assessments"],
    )

    y -= 0.8 * cm

    _draw_line(
        c,
        y,
        "Incorrect Assessments",
        report_data["incorrect_assessments"],
    )

    y -= 1.2 * cm

    c.setFont(
        "Helvetica-Bold",
        11,
    )

    c.drawString(
        2.5 * cm,
        y,
        "Assessment Scores",
    )

    y -= 0.7 * cm

    c.setFont(
        "Helvetica",
        10,
    )

    for assessment in report_data[
        "assessment_scores"
    ]:

        text = (
            f"{assessment['expected_sign']} → "
            f"{assessment['predicted_sign']} : "
            f"{assessment['score']}%"
        )

        c.drawString(
            3 * cm,
            y,
            text,
        )

        y -= 0.6 * cm

        if y < 3 * cm:
            c.showPage()

            y = A4[1] - 3 * cm

    return _finish_pdf(
        c,
        file_path,
    )


# ---------------------------------------------------------
# 3. ACCURACY REPORT PDF
# ---------------------------------------------------------

def generate_accuracy_report_pdf(
    learner_name: str,
    report_data: dict,
    user_id: str,
) -> str:

    c, file_path = _create_pdf(
        filename=f"Accuracy_Report_{user_id}.pdf",
        title="Accuracy Report",
        learner_name=learner_name,
    )

    y = A4[1] - 5 * cm

    _draw_line(
        c,
        y,
        "Overall Accuracy",
        f"{report_data['overall_accuracy']}%",
    )

    y -= 1.2 * cm

    c.setFont(
        "Helvetica-Bold",
        11,
    )

    c.drawString(
        2.5 * cm,
        y,
        "Accuracy by Letter",
    )

    y -= 0.7 * cm

    c.setFont(
        "Helvetica",
        10,
    )

    for letter, score in report_data[
        "letter_accuracy"
    ].items():

        c.drawString(
            3 * cm,
            y,
            f"{letter}: {score}%",
        )

        y -= 0.6 * cm

        if y < 4 * cm:
            c.showPage()
            y = A4[1] - 3 * cm

    y -= 0.5 * cm

    _draw_line(
        c,
        y,
        "Strong Letters",
        ", ".join(
            report_data["strong_letters"]
        ) or "None",
    )

    y -= 0.8 * cm

    _draw_line(
        c,
        y,
        "Weak Letters",
        ", ".join(
            report_data["weak_letters"]
        ) or "None",
    )

    return _finish_pdf(
        c,
        file_path,
    )


# ---------------------------------------------------------
# 4. CERTIFICATION REPORT PDF
# ---------------------------------------------------------

def generate_certification_report_pdf(
    learner_name: str,
    report_data: dict,
    user_id: str,
) -> str:

    c, file_path = _create_pdf(
        filename=f"Certification_Report_{user_id}.pdf",
        title="Certification Report",
        learner_name=learner_name,
    )

    y = A4[1] - 5 * cm

    _draw_line(
        c,
        y,
        "Certification Status",
        report_data["certificate_status"],
    )

    y -= 0.8 * cm

    _draw_line(
        c,
        y,
        "Certificates Earned",
        report_data["certificates_earned"],
    )

    y -= 1.2 * cm

    c.setFont(
        "Helvetica-Bold",
        11,
    )

    c.drawString(
        2.5 * cm,
        y,
        "Certificate History",
    )

    y -= 0.8 * cm

    c.setFont(
        "Helvetica",
        10,
    )

    if not report_data["certificates"]:

        c.drawString(
            3 * cm,
            y,
            "No certificates earned.",
        )

    else:

        for certificate in report_data[
            "certificates"
        ]:

            c.drawString(
                3 * cm,
                y,
                f"Certificate: "
                f"{certificate['certificate_code']}",
            )

            y -= 0.6 * cm

            c.drawString(
                3 * cm,
                y,
                f"Average Score: "
                f"{certificate['average_score']}%",
            )

            y -= 0.6 * cm

            c.drawString(
                3 * cm,
                y,
                f"Valid: "
                f"{certificate['is_valid']}",
            )

            y -= 1 * cm

            if y < 4 * cm:
                c.showPage()
                y = A4[1] - 3 * cm

    return _finish_pdf(
        c,
        file_path,
    )