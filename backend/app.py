from flask import Flask
from flask_cors import CORS
from extensions import db
from models.category import seed_categories

# ---------- [USR-BE-01] User model ----------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # [USR-BE-04] Hash passwords: never store plain text
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        # password_hash is deliberately excluded
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ---------- JWT helpers ----------
def create_token(user):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "iat": now,
        "exp": now + timedelta(minutes=app.config["JWT_EXPIRES_MINUTES"]),
    }
    return jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")

# ---------- [USR-BE-02] Registration ----------
@app.post("/api/users/register")
def register():
    body = request.get_json(silent=True) or {}
    username = (body.get("username") or "").strip()
    email = (body.get("email") or "").strip().lower()
    password = body.get("password") or ""

    errors = {}
    if not 3 <= len(username) <= 50:
        errors["username"] = "Username must be 3-50 characters"
    if not EMAIL_RE.match(email):
        errors["email"] = "A valid email is required"
    if len(password) < 8:
        errors["password"] = "Password must be at least 8 characters"
    if errors:
        return fail("Validation failed", 422, errors)

    if User.query.filter_by(username=username).first():
        return fail("Username already taken", 409, {"username": "Already taken"})
    if User.query.filter_by(email=email).first():
        return fail("Email already registered", 409, {"email": "Already registered"})

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return ok(user.to_dict(), "User registered", 201)


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    CORS(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        seed_categories()

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
