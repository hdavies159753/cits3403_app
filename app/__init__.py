from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app import models  # noqa: F401 — ensure models are registered with SQLAlchemy

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        _seed_admin()

    return app


def _seed_admin():
    """Create the default admin account if it doesn't already exist."""
    from app.models import User
    try:
        if not User.query.filter_by(username='adminuser').first():
            admin = User(username='adminuser')
            admin.set_password('adminuserpass')
            db.session.add(admin)
            db.session.commit()
    except Exception:
        pass  # table may not exist yet (e.g. during flask db upgrade)
