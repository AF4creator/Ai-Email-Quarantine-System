from flask import Blueprint, render_template, session, redirect, url_for, flash
from app import db
from app.database.model import QuarantinedEmail, User, Whitelist
from app.emails.fetcher import connect_imap, fetch_inbox
from app.emails.pipeline import process_fetched_emails
from app.utils.helpers import decrypt_imap_password
from app.emails.scan_service import run_scan_for_user

emails = Blueprint("emails", __name__, url_prefix="/emails")


# ---------------- LOGIN CHECK ----------------
def require_login():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return None


# ---------------- SAFE EMAILS ----------------
@emails.route("/safe")
def safe_emails():
    check = require_login()
    if check:
        return check

    emails_list = QuarantinedEmail.query.filter_by(
        user_id=session["user_id"],
        classification="safe",
        status="active"
    ).all()

    return render_template("email_list.html", emails=emails_list, category="Safe Emails")


# ---------------- SUSPICIOUS EMAILS ----------------
@emails.route("/suspicious")
def suspicious_emails():
    check = require_login()
    if check:
        return check

    emails_list = QuarantinedEmail.query.filter_by(
        user_id=session["user_id"],
        classification="suspicious",
        status="active"
    ).all()

    return render_template("email_list.html", emails=emails_list, category="Suspicious Emails")


# ---------------- QUARANTINED EMAILS ----------------
@emails.route("/quarantine")
def quarantined_emails():
    check = require_login()
    if check:
        return check

    emails_list = QuarantinedEmail.query.filter_by(
        user_id=session["user_id"],
        classification="quarantined",
        status="active"
    ).all()

    return render_template("email_list.html", emails=emails_list, category="Quarantined Emails")


# ---------------- EMAIL DETAIL VIEW ----------------
@emails.route("/view/<int:email_id>")
def view_email(email_id):
    check = require_login()
    if check:
        return check

    email = QuarantinedEmail.query.filter_by(
        email_id=email_id,
        user_id=session["user_id"]
    ).first_or_404()

    return render_template("email_detail.html", email=email)


# ---------- RELEASE ----------
@emails.route("/release/<int:email_id>", methods=["POST"])
def release_email(email_id):
    check = require_login()
    if check:
        return check

    email = QuarantinedEmail.query.filter_by(
        email_id=email_id,
        user_id=session["user_id"]
    ).first_or_404()

    email.status = "released"
    db.session.commit()

    flash("Email released successfully.", "success")
    return redirect(url_for("dashboard.home"))


# ---------- DELETE ----------
@emails.route("/delete/<int:email_id>", methods=["POST"])
def delete_email(email_id):
    check = require_login()
    if check:
        return check

    email = QuarantinedEmail.query.filter_by(
        email_id=email_id,
        user_id=session["user_id"]
    ).first_or_404()

    email.status = "deleted"
    db.session.commit()

    flash("Email deleted permanently.", "danger")
    return redirect(url_for("dashboard.home"))


# ---------- WHITELIST ----------
@emails.route("/whitelist/<int:email_id>", methods=["POST"])
def whitelist_email(email_id):
    check = require_login()
    if check:
        return check

    email = QuarantinedEmail.query.filter_by(
        email_id=email_id,
        user_id=session["user_id"]
    ).first_or_404()

    exists = Whitelist.query.filter_by(
        user_id=email.user_id,
        sender_email=email.sender
    ).first()

    if not exists:
        w = Whitelist(
            user_id=email.user_id,
            sender_email=email.sender
        )
        db.session.add(w)

    db.session.commit()

    flash("Sender added to whitelist.", "success")
    return redirect(url_for("dashboard.home"))


# ---------------- SCAN MAILBOX ----------------
@emails.route("/scan")
def scan_mailbox():
    check = require_login()
    if check:
        return check

    user_id = session["user_id"]
    user = User.query.get_or_404(user_id)

    mail = connect_imap(
        user.imap_server,
        user.imap_port,
        user.imap_email,
        decrypt_imap_password(user.imap_password_enc)
    )

    fetched_emails = fetch_inbox(mail)

    new_count = process_fetched_emails(user_id, fetched_emails)

    run_scan_for_user(user_id)

    flash(f"Scan completed successfully. {new_count} new emails processed.", "success")

    return redirect(url_for("dashboard.user_home"))
