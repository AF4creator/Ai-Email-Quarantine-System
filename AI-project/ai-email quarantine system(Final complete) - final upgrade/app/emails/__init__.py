import imaplib 

class IMAPClient:
    def __init__(self, host, username, imap_password, port=993):
        self.conn = imaplib.IMAP4_SSL(host, port)
        self.conn.login(username, imap_password)

    def select_folder(self, folder="INBOX"):
        self.conn.select(folder)

    def search(self, criteria='ALL'):
        result, data = self.conn.search(None, criteria)
        return data[0].split()

    def fetch(self, msg_id):
        result, data = self.conn.fetch(msg_id, "(RFC822)")
        return data

    def move(self, msg_id, folder):
        self.conn.copy(msg_id, folder)
        self.conn.store(msg_id, '+FLAGS', '\\Deleted')
        self.conn.expunge()

    def logout(self):
        self.conn.logout()
