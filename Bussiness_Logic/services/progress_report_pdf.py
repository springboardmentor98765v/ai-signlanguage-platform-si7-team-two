"""
Progress Report PDF Generator — Day 8.
Reuses the same ReportLab approach as certificate_generator.py to
produce a simple, clean summary PDF of a learner's journey.
"""
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas

REPORTS_DIR = "generated_reports"

def generate_progress_report_pdf(learner_name: str, report_data: dict, user_id: str) -> str:
    os.makedirs(REPORTS_DIR, exist_ok=True)
    filename = f"progress_{user_id}.pdf"
    file_path = os.path.join(REPORTS_DIR, filename)

    page_width, page_height = A4
    c = canvas.Canvas(file_path, pagesize=A4)

    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(colors.HexColor("#2C3E50"))
    c.drawCentredString(page_width / 2, page_height - 3 * cm, "Learner Progress Report")

    c.setFont("Helvetica", 14)
    c.setFillColor(colors.black)
    c.drawCentredString(page_width / 2, page_height - 4 * cm, learner_name or "Learner")

    y = page_height - 6 * cm
    line_height = 0.9 * cm

    def draw_line(label, value):
        nonlocal y
        c.setFont("Helvetica-Bold", 12)
        c.drawString(2.5 * cm, y, f"{label}:")
        c.setFont("Helvetica", 12)
        c.drawString(8 * cm, y, str(value))
        y -= line_height

    draw_line("Lessons Completed", report_data["lessons_completed"])
    draw_line("Average Accuracy", f"{report_data['average_accuracy']}%")
    draw_line("Total Attempts", report_data["total_attempts"])
    draw_line("Total Practice Time (sec)", report_data["total_practice_time"])
    draw_line("Letters Attempted", ", ".join(report_data["attempted_letters"]) or "None")
    draw_line("Weak Letters", ", ".join(report_data["weak_letters"]) or "None")
    draw_line("Certificates Earned", len(report_data["certificates_earned"]))

    today_str = datetime.utcnow().strftime("%B %d, %Y")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.grey)
    c.drawString(2.5 * cm, 2 * cm, f"Generated on {today_str}")

    c.save()
    return file_path