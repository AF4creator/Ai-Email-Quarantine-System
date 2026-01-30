from flask import Blueprint
from . import quarantine_bp

quarantine_bp= Blueprint("quarantine", __name__)

@quarantine_bp.route("/quarantine")
def quarantine_home():
    return "Quarantine Page Working"
