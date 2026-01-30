def decide_action(score: float):
    if score < 0.3:
        return "safe"
    elif score < 0.7:
        return "suspicious"
    else:
        return "quarantined"

def move_email(conn, msg_uid, folder):
    conn.copy(msg_uid, folder)
    conn.store(msg_uid, '+FLAGS', '\\Deleted')
    conn.expunge()
