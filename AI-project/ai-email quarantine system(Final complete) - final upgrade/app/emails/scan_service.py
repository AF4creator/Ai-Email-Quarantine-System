from app.database import db
from app.database.model import ScanLog, QuarantinedEmail

def run_scan_for_user(user_id):
    # Count results AFTER scan
    total_safe = QuarantinedEmail.query.filter_by(
        user_id=user_id,
        classification="safe"
    ).count()

    total_suspicious = QuarantinedEmail.query.filter_by(
        user_id=user_id,
        classification="suspicious"
    ).count()

    total_quarantined = QuarantinedEmail.query.filter_by(
        user_id=user_id,
        classification="quarantined"
    ).count()

    total_scanned = total_safe + total_suspicious + total_quarantined
    # SAVE TO scan_logs TABLE
    scan_log = ScanLog(
        user_id=user_id,
        total_scanned=total_scanned,
        total_safe=total_safe,
        total_suspicious=total_suspicious,
        total_quarantined=total_quarantined
    )

    db.session.add(scan_log)
    db.session.commit()

    return scan_log
