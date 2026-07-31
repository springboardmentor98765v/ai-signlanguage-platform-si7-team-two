from pathlib import Path
from datetime import datetime
from openpyxl import Workbook


EXPORT_DIR = Path("generated_reports")
EXPORT_DIR.mkdir(exist_ok=True)


def generate_progress_report_excel(
    learner_name: str,
    report_data: dict,
    user_id: str,
):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Progress Report"

    sheet["A1"] = "Learner Progress Report"

    sheet.append([])
    sheet.append(["Learner Name", learner_name])
    sheet.append(["User ID", user_id])
    sheet.append(["Generated At", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")])

    sheet.append([])

    sheet.append(["Lessons Completed", report_data["lessons_completed"]])
    sheet.append(["Total Practice Time (Seconds)", report_data["total_practice_time"]])
    sheet.append(["Average Accuracy (%)", report_data["average_accuracy"]])
    sheet.append(["Total Attempts", report_data["total_attempts"]])

    sheet.append([])

    sheet.append([
        "Attempted Letters",
        ", ".join(report_data["attempted_letters"])
    ])

    sheet.append([
        "Weak Letters",
        ", ".join(report_data["weak_letters"])
    ])

    sheet.append([])

    sheet.append([
        "Certificate Code",
        "Average Score",
        "Issued At"
    ])

    for certificate in report_data["certificates_earned"]:
        sheet.append([
            certificate["certificate_code"],
            certificate["average_score"],
            str(certificate["issued_at"])
            if certificate["issued_at"]
            else "-"
        ])

    file_path = EXPORT_DIR / f"Progress_Report_{user_id}.xlsx"

    workbook.save(file_path)

    return str(file_path)

def generate_instructor_summary_excel(learners):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Instructor Summary"

    sheet.append([
        "Learner ID",
        "Lessons Completed",
        "Average Accuracy",
        "Total Attempts",
        "Certificates Earned"
    ])

    for learner in learners:
        sheet.append([
            learner["user_id"],
            learner["lessons_completed"],
            learner["average_accuracy"],
            learner["total_attempts"],
            learner["certificates_earned"],
        ])

    file_path = EXPORT_DIR / "Instructor_Summary.xlsx"

    workbook.save(file_path)

    return str(file_path)