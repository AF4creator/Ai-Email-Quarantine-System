from flask import Blueprint
from .import routes

dashboard_bp = Blueprint("dashboard", __name__, template_folder="../templates", static_folder="../static")


