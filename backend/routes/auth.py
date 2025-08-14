from flask import Blueprint, request, jsonify, current_app
from passlib.hash import bcrypt
import jwt, time
from sqlalchemy import create_engine, text
import os

auth_bp = Blueprint("auth", __name__)

DB_URL = os.getenv("AUTH_DB_URL", "sqlite:///users.db")
engine = create_engine(DB_URL, future=True)

# Create users table if missing
with engine.begin() as conn:
    conn.exec_driver_sql(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at INTEGER NOT NULL
        );
        """
    )

def make_token(email: str, exp_min: int) -> str:
    payload = {"sub": email, "iat": int(time.time()), "exp": int(time.time()) + exp_min * 60}
    return jwt.encode(payload, current_app.config["JWT_SECRET"], algorithm="HS256")


@auth_bp.post("/signup")
def signup():
    data = request.get_json(force=True)
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    if not email or not password:
        return jsonify({"error": "email and password required"}), 400

    pwd_hash = bcrypt.hash(password)
    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO users (email, password_hash, created_at) VALUES (:e, :p, :t)"),
                {"e": email, "p": pwd_hash, "t": int(time.time())}
            )
    except Exception:
        return jsonify({"error": "email already exists"}), 409

    token = make_token(email, current_app.config["JWT_EXP_MIN"])
    return jsonify({"token": token, "email": email})


@auth_bp.post("/login")
def login():
    data = request.get_json(force=True)
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    with engine.begin() as conn:
        row = conn.execute(text("SELECT password_hash FROM users WHERE email=:e"), {"e": email}).fetchone()
        if not row or not bcrypt.verify(password, row[0]):
            return jsonify({"error": "invalid credentials"}), 401
    token = make_token(email, current_app.config["JWT_EXP_MIN"])
    return jsonify({"token": token, "email": email})


def require_jwt(fn):
    from functools import wraps

    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "missing bearer token"}), 401
        token = auth.split(" ", 1)[1]
        try:
            jwt.decode(token, current_app.config["JWT_SECRET"], algorithms=["HS256"])
        except Exception:
            return jsonify({"error": "invalid or expired token"}), 401
        return fn(*args, **kwargs)

    return wrapper
