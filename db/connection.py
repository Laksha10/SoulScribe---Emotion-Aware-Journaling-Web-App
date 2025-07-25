from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Shared instances
db = SQLAlchemy()
mail = Mail()

def init_extensions(app):
    """Initialize all shared extensions (DB, Mail, etc.)"""
    # Database config
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Mail config
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER", "SoulScribe <noreply@soulscribe.app>")

    # Init extensions
    db.init_app(app)
    mail.init_app(app)
