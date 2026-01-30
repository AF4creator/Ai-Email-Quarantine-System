from flask import Blueprint, send_file, session, redirect, url_for
from app.reports.report_service import (build_report_data, generate_pdf, generate_docx, generate_txt)
import os
import tempfile

reports = Blueprint("reports", __name__, url_prefix="/reports")


@reports.route("/download/<format>")
def download_report(format):
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))

    report = build_report_data(user_id)
    if not report:
        return redirect(url_for("dashboard.user_home"))

    temp_dir = tempfile.gettempdir()
    filename = f"scan_report_{user_id}.{format}"
    filepath = os.path.join(temp_dir, filename)

    if format == "pdf":
        generate_pdf(report, filepath)
    elif format == "docx":
        generate_docx(report, filepath)
    elif format == "txt":
        generate_txt(report, filepath)
    else:
        return redirect(url_for("dashboard.user_home"))

    return send_file(filepath, as_attachment=True)
