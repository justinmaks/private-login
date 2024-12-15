from flask import Flask
from flask_talisman import Talisman
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    # Add security headers with Talisman
    csp = {
        'default-src': ["'self'"],
        'script-src': ["'self'", "'unsafe-inline'"],
        'style-src': ["'self'", "'unsafe-inline'"],
    }

    # Enable HTTPS in production, disable in development
    if app.config.get("ENV") == "production":
        Talisman(app, content_security_policy=csp)
    else:
        Talisman(app, content_security_policy=csp, force_https=False)

    # Register Blueprints
    from .auth import auth_bp
    from .main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    print(app.config["SQLALCHEMY_DATABASE_URI"])


    with app.app_context():
        db.create_all()

    return app
