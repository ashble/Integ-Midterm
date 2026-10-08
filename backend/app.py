from flask import Flask
from flask_cors import CORS
from extensions import db
from models.category import seed_categories


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
