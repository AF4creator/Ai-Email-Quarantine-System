from datetime import datetime
from app.database import db


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    imap_server = db.Column(db.String(255), nullable=False)
    imap_port = db.Column(db.Integer, default=993)
    imap_email = db.Column(db.String(255), nullable=False)
    imap_password_enc = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    scan_logs = db.relationship("ScanLog", backref="user", lazy=True)


class QuarantinedEmail(db.Model):
    __tablename__ = "quarantined_emails"

    email_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    message_uid = db.Column(db.String(100), nullable=False)
    sender = db.Column(db.String(255))
    subject = db.Column(db.String(255))
    body = db.Column(db.Text)
    received_at = db.Column(db.String(100))
    quarantined_at = db.Column(db.DateTime, default=datetime.utcnow)
    classification = db.Column(db.String(50))  # safe / suspicious / quarantined
    spam_score = db.Column(db.Float)
    url_status = db.Column(db.String(50))
    status = db.Column(db.String(20), default="active")

    __table_args__ = (
        db.UniqueConstraint("user_id", "message_uid", name="uq_user_message"),
    )


class ScanLog(db.Model):
    __tablename__ = "scan_logs"

    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.user_id", ondelete="CASCADE"),nullable=False)

    total_scanned = db.Column(db.Integer, nullable=False)
    total_quarantined = db.Column(db.Integer, nullable=False)
    total_suspicious = db.Column(db.Integer, nullable=False)
    total_safe = db.Column(db.Integer, nullable=False)

    scan_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Whitelist(db.Model):
    __tablename__ = "whitelist"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    sender_email = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
