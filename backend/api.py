import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "my secret"
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://postgres:{os.environ['POSTGRES_PASSWORD']}@postgres:5432/{os.environ['POSTGRES_DB']}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("applications.id"))
    name = db.Column(db.String(100), unique=True)
    version = db.Column(db.String(100))
    stack = db.Column(db.String(100))
    description = db.Column(db.Text)
    team = db.Column(db.String(100))
    owner = db.Column(db.String(120))
    eks_size = db.Column(db.String(100))

    # Relationships
    children = db.relationship(
        "Application", backref=db.backref("parent_app", remote_side=[id])
    )

with app.app_context():
    db.create_all()

@app.route("/api/test", methods=["GET"])
def testing():
    return jsonify({"status": "success", "message": "testing!"})
