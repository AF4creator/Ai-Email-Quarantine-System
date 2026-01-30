import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY","dev-secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "mysql+mysqlconnector://root@localhost/email_db(test)")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

