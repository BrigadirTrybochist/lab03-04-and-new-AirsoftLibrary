"""Application factory and entry point for the project.

This module creates the Flask `app` object, initializes the database and
registers the routes blueprint defined in `routes.py`.
"""

import logging
import os
from flask import Flask
from models import db
from flask_wtf.csrf import CSRFProtect, generate_csrf

# Basic logging
logging.basicConfig(level=logging.DEBUG)


def create_app():
    app = Flask(__name__)

    # Configuration: use absolute path for SQLite database to avoid path/lock issues
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'airsoft_collection.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path.replace('\\', '/')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev'  # change in production

    # Initialize DB
    db.init_app(app)

    # Enable CSRF protection and expose csrf_token() to templates
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Expose generate_csrf as template global for {{ csrf_token() }}
    app.jinja_env.globals['csrf_token'] = generate_csrf

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.error(f"Database initialization error: {e}")

    # Register routes blueprint
    try:
        from routes import bp as routes_bp
        app.register_blueprint(routes_bp)
    except Exception as e:
        app.logger.error(f"Could not register routes blueprint: {e}")

    return app


# Create app instance for direct runs and imports
app = create_app()


if __name__ == '__main__':
    # Run with debug on for development
    app.run(debug=True)