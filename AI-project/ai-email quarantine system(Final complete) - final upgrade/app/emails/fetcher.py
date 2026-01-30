import imaplib
import email

def connect_imap(server, port, username, imap_password):
    mail = imaplib.IMAP4_SSL(server, port)
    mail.login(username, imap_password)
    return mail


def fetch_inbox(mail, limit=20):
    """
    Fetch emails using IMAP UID (stable, prevents duplicates)
    """
    mail.select("INBOX")

    status, data = mail.uid("search", None, "ALL")
    if status != "OK":
        return []

    uids = data[0].split()
    emails = []

    for uid in uids[-limit:]:
        status, msg_data = mail.uid("fetch", uid, "(RFC822)")
        if status != "OK":
            continue

        msg = email.message_from_bytes(msg_data[0][1])
        emails.append((uid.decode(), msg))

    return emails
