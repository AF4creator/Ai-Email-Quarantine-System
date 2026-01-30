from flask import Flask
from .database import db
from .auth.routes import auth
from .dashboard.routes import dashboard
from .quarantine.routes import quarantine_bp
from .emails.routes import emails
from .reports.routes import reports
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(quarantine_bp)
    app.register_blueprint(emails)
    app.register_blueprint(reports)

    
    return app


