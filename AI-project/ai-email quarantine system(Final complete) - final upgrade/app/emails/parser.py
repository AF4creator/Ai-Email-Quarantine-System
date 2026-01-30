from bs4 import BeautifulSoup

def extract_text(msg):
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain" and not part.get_filename():
                body += part.get_payload(decode=True).decode(errors="ignore")

            elif content_type == "text/html" and not part.get_filename():
                html = part.get_payload(decode=True)
                soup = BeautifulSoup(html, "html.parser")
                body += soup.get_text(separator=" ")
    else:
        body = msg.get_payload(decode=True).decode(errors="ignore")

    return body.strip()
