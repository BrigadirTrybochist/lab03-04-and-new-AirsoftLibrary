import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Test database connection and configure appropriately
def get_working_database_uri():
    """Test PostgreSQL connection and fallback to SQLite if needed"""
    postgres_url = os.environ.get("DATABASE_URL")
    
    if postgres_url and not postgres_url.startswith("sqlite://"):
        try:
            # Test PostgreSQL connection
            import psycopg2
            from urllib.parse import urlparse
            
            parsed = urlparse(postgres_url)
            
            # Quick connection test
            test_conn = psycopg2.connect(
                host=parsed.hostname,
                port=parsed.port,
                user=parsed.username,
                password=parsed.password,
                database=parsed.path[1:]  # Remove leading slash
            )
            test_conn.close()
            
            print("PostgreSQL connection successful")
            return postgres_url
            
        except Exception as e:
            print(f"PostgreSQL connection failed: {e}")
            print("Falling back to SQLite database...")
    
    # Default to SQLite file inside this package's instance folder
    instance_db = os.path.join(os.path.dirname(__file__), 'instance', 'airsoft_collection.db')
    return f"sqlite:///{instance_db}"

# Configure the database with working connection
database_url = get_working_database_uri()
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
# SQLAlchemy engine options
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
# Import models (models defines `db`) and initialize the extension
import models
db = models.db
db.init_app(app)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Import routes (after db is available)
import routes

# Initialize database tables
with app.app_context():
    db.create_all()
    print(f"Database tables created successfully using: {database_url.split('://')[0]}://...")
