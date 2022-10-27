import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "my secret"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://postgres:{os.environ['POSTGRES_PASSWORD']}@postgres:5432/{os.environ['POSTGRES_DB']}"
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

    @property
    def get_child(self):
        return len(self.children)

    def add_dependent_app(self, application):
        if (
            not self.is_dependency_of(application)
            and not application.is_dependency_of(self)
            and self is not application
        ):
            self.children.append(application)

    def remove_dependent_app(self, application):
        if application.is_dependency_of(self):
            self.children.remove(application)

    def is_dependency_of(self, application):
        return self.parent_app == application

    def has_parent(self):
        return bool(self.parent_app)

    def is_parent(self):
        return self.parent_id == self.id

    def get_siblings(self):
        return Application.query.filter(
            Application.parent_id == self.parent_id, Application.id != self.id
        ).all()

    @property
    def depends_on(self):
        return self.children

    def __repr__(self):
        return f'<Application "{self.name}">'
