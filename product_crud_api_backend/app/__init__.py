from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from .routes.health import blp as health_blp
from .routes.products import blp as products_blp
from .models import db
import os


# PUBLIC_INTERFACE
def create_app() -> Flask:
    """Create and configure the Flask application.

    Configures:
    - CORS for all routes
    - Flask-Smorest API and Swagger UI at /docs
    - SQLAlchemy with SQLite default (override via DATABASE_URL env)
    Registers:
    - Health check blueprint at /
    - Products CRUD blueprint at /products
    """
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    CORS(app, resources={r"/*": {"origins": "*"}})

    # OpenAPI/Docs configuration
    app.config["API_TITLE"] = "Product CRUD API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Database configuration: use SQLite by default
    database_url = os.getenv("DATABASE_URL", "sqlite:///products.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init extensions
    db.init_app(app)
    api = Api(app)

    # Register blueprints
    api.register_blueprint(health_blp)
    api.register_blueprint(products_blp)

    # Create tables if not exist
    with app.app_context():
        db.create_all()

    return app


# Maintain existing import path compatibility: expose 'app'
app = create_app()
