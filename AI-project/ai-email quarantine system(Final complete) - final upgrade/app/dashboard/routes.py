from flask import Blueprint, render_template, session, redirect, url_for
from app.database.model import QuarantinedEmail, ScanLog

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
def home():
    user_id = session.get("user_id")
    user_name = session.get("user_name")

    if not user_id:
        return redirect(url_for("auth.login"))

    quarantined = QuarantinedEmail.query.filter_by(
        user_id=user_id,
        classification="quarantined",
        status="active"
    ).count()

    suspicious = QuarantinedEmail.query.filter_by(
        user_id=user_id,
        classification="suspicious",
        status="active"
    ).count()

    safe = QuarantinedEmail.query.filter_by(
        user_id=user_id,
        classification="safe",
        status="active"
    ).count()

    return render_template(
        "dashboard.html",
        user_name=user_name,
        quarantined_count=quarantined,
        suspicious_count=suspicious,
        safe_count=safe,
    )


@dashboard.route("/user-home")
def user_home():
    user_id = session.get("user_id")
    user_name = session.get("user_name")

    if not user_id:
        return redirect(url_for("auth.login"))

    # Get latest scan log
    scan = (
        ScanLog.query.filter_by(user_id=user_id)
        .order_by(ScanLog.scan_date.desc())
        .first()
    )

    # If no scan yet, send zero values
    if not scan:
        scan_data = {
            "total_safe": 0,
            "total_suspicious": 0,
            "total_quarantined": 0,
            "total_scanned": 0,
            "scan_date": None
        }
    else:
        scan_data = {
            "total_safe": scan.total_safe,
            "total_suspicious": scan.total_suspicious,
            "total_quarantined": scan.total_quarantined,
            "total_scanned": scan.total_scanned,
            "scan_date": scan.scan_date
        }

    return render_template(
        "user_home.html",
        user_name=user_name,
        scan=scan_data
    )
