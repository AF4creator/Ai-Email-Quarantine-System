SPAM_THRESHOLD = 0.8
SUSP_THRESHOLD = 0.6

def classify_email(score):
    if score >= SPAM_THRESHOLD:
        return "QUARANTINE"
    elif score >= SUSP_THRESHOLD:
        return "SUSPICIOUS"
    return "SAFE"
