from app.database.model import User
from app.emails.fetcher import connect_imap, fetch_inbox
from app.emails.parser import parse_email
from app.ml.predict import predict_spam
from app.quarantine.manager import decide_action, move_email
from app.utils.helpers import decrypt_imap_password
from app.database import db

# Fetch a user from DB
user = User.query.filter_by(email="user@gmail.com").first()

if user:
    # Decrypt IMAP password
    real_password = decrypt_imap_password(user.imap_password_enc)

    # Connect to IMAP
    mail = connect_imap(user.imap_server, user.imap_port, user.imap_email, real_password)

    # Fetch latest 20 emails
    emails = fetch_inbox(mail)

    for msg_id, msg in emails:
        parsed = parse_email(msg)
        score = predict_spam(parsed["body"])
        decision = decide_action(score)

        if decision == "QUARANTINE":
            move_email(mail, msg_id, "Quarantine")
