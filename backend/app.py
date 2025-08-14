import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from .routes.auth import auth_bp
from .routes.clause_analysis import clause_bp
from .routes.risk_analyzer import risk_bp
from .routes.document_classification import doc_class_bp
from .routes.ner_extraction import ner_bp

# Load environment variables from .env
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

# Configs
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
app.config["JWT_SECRET"] = os.getenv("JWT_SECRET", "dev-jwt")
app.config["JWT_EXP_MIN"] = int(os.getenv("JWT_EXP_MIN", "120"))

# Import Blueprints


# Register Blueprints with URL prefixes
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(clause_bp, url_prefix="/api/clause")
app.register_blueprint(risk_bp, url_prefix="/api/risk")
app.register_blueprint(doc_class_bp, url_prefix="/api/document")
app.register_blueprint(ner_bp, url_prefix="/api/ner")

# Health check endpoint
@app.route("/health")
def health():
    return {"status": "ok"}

# Run server
if __name__ == "__main__":
    debug_mode = os.getenv("DEBUG", "True") == "True"
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
