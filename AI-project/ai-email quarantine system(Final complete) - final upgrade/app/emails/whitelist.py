from app.database.model import Whitelist

def is_whitelisted(user_id, sender):
    record = Whitelist.query.filter_by(user_id=user_id, sender_email=sender).first()

    return record is not None
