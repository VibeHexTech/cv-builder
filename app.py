from flask import Flask, jsonify

from cv_builder.api_routes import api
from cv_builder.config import Config
from cv_builder.database import initialize_database
from cv_builder.docx_routes import docx_bp
from cv_builder.extensions import db
from cv_builder.models import CvEntry
from cv_builder.services.docx_parser import extract_docx_rows
from cv_builder.web_routes import web_bp


def create_app(config_class=Config):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_class)

    db.init_app(app)
    app.register_blueprint(web_bp)
    app.register_blueprint(docx_bp)
    api.init_app(app)

    initialize_database(app)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
