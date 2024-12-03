from flask import Flask
from app.routes.routes import routes_bp

def create_app():
    app = Flask(__name__)

    # Registro de blueprints
    app.register_blueprint(routes_bp)

    return app
