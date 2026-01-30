import logging
from email.header import decode_header
from app.database import db
from app.database.model import QuarantinedEmail, Whitelist
from app.emails.parser import extract_text
from app.features.url_feature import check_urls
from app.ml.predict import predict_spam

logger = logging.getLogger(__name__)

def clean_subject(subject):
    if not subject:
        return "(No Subject)"
    decoded, charset = decode_header(subject)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(charset or "utf-8", errors="ignore")
    return decoded

def process_email(user_id, email_uid, msg):
    try:
        exists = QuarantinedEmail.query.filter_by(user_id=user_id, message_uid=email_uid).first()
        if exists:
            return False

        sender = msg.get("From", "")
        subject = clean_subject(msg.get("Subject"))
        received_at = msg.get("Date")
        body = extract_text(msg)
        urls = check_urls(body)

        if Whitelist.query.filter_by(user_id=user_id, sender_email=sender).first():
            spam_score = 0.0
            classification = "safe"
        else:
            spam_score = predict_spam(body, "", urls)
            if spam_score > 0.8:
                classification = "quarantined"
            elif spam_score > 0.6:
                classification = "suspicious"
            else:
                classification = "safe"

        email = QuarantinedEmail(
            user_id=user_id,
            message_uid=email_uid,
            sender=sender,
            subject=subject,
            body=body,
            received_at=received_at,
            spam_score=float(spam_score),
            url_status="Found" if urls else "None",
            classification=classification,
            status="active"
        )

        db.session.add(email)
        db.session.commit()
        return True

    except Exception as e:
        logger.error(f"Failed to process email UID {email_uid}: {e}")
        db.session.rollback()
        return False

def process_fetched_emails(user_id, fetched_emails):
    new_count = 0
    for uid, msg in fetched_emails:
        if process_email(user_id, uid, msg):
            new_count += 1
        else:
            logger.warning(f"Skipping email UID {uid} due to processing error or duplicate.")
    return new_count
