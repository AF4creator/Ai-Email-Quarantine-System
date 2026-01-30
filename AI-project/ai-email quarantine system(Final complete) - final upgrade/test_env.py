from dotenv import load_dotenv
import os

load_dotenv()
print("FERNET_KEY:", os.getenv("FERNET_KEY"))
