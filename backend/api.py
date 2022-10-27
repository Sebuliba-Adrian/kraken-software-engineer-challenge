import os
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy

from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin


import os

app = Flask(__name__)
cors = CORS(app)

app.config["SECRET_KEY"] = "my secret"
app.config["CORS_HEADERS"] = "Content-Type"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://postgres:{os.environ['POSTGRES_PASSWORD']}@postgres:5432/{os.environ['POSTGRES_DB']}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


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
            return True
        return False

    def remove_dependent_app(self, application):
        if application.is_dependency_of(self):
            self.children.remove(application)
            return True
        return False

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

    def to_dict(self):
        result = {
            "name": self.name,
            "version": self.version,
            "stack": self.stack,
            "description": self.description,
            "team": self.team,
            "owner": self.owner,
            "eks_size": self.eks_size,
        }

        if self.get_child > 0:
            holder = []
            for child in self.children:
                holder.append(child.name)
                result["depends-on"] = holder

        return result

    @property
    def depends_on(self):
        return self.children

    def __repr__(self):
        return f'<Application "{self.name}">'


@app.route("/api/apps", methods=["GET"])
@cross_origin()
def get_apps():
    apps = [app.to_dict() for app in db.session.query(Application).all()]
    return jsonify(apps)


@app.route("/api/apps", methods=["POST"])
@cross_origin()
def create_app():
    body = request.get_json()
    db.session.add(
        Application(
            name=body["name"],
            version=body["version"],
            stack=body["stack"],
            description=body["description"],
            team=body["team"],
            owner=body["owner"],
            eks_size=body["eks_size"],
        )
    )
    db.session.commit()
    return make_response(jsonify({"app": "success"}), 201)


@app.route("/api/apps/<int:id>", methods=["GET"])
@cross_origin()
def get_app(id):
    app = Application.query.get(id)
    return jsonify({"data": app.to_dict()})


@app.route("/api/apps/<int:id>", methods=["PUT"])
@cross_origin()
def update_app(id):
    body = request.get_json()
    db.session.query(Application).filter_by(id=id).update(
        dict(
            name=body["name"],
            version=body["version"],
            stack=body["stack"],
            description=body["description"],
            team=body["team"],
            owner=body["owner"],
            eks_size=body["eks_size"],
        )
    )
    db.session.commit()
    return jsonify({"success": True, "message": "application updated "})


@app.route("/api/apps/<int:id>", methods=["DELETE"])
@cross_origin()
def delete_app(id):
    db.session.query(Application).filter_by(id=id).delete()
    db.session.commit()
    return jsonify({"success": True, "message": "application deleted "})


@app.route("/api/apps/<int:id>/dependencies/<int:dependency_id>", methods=["POST"])
@cross_origin()
def add_app_dependencies(id, dependency_id):
    app = Application.query.get(id)
    dep_app = Application.query.get(dependency_id)
    if app.add_dependent_app(dep_app):
        db.session.commit()
        return (
            jsonify({"success": True, "message": "dependency added"}),
            201,
        )
    return jsonify({"success": False, "message": "dependency could not be added."}), 400


@app.route("/api/apps/<int:id>/dependencies", methods=["GET"])
@cross_origin()
def get_app_dependencies(id):
    app = Application.query.get(id)

    return jsonify(app.depends_on)


@app.route("/api/apps/<int:id>/dependencies/<int:dependency_id>", methods=["DELETE"])
@cross_origin()
def delete_app_dependency(id, dependency_id):
    app = Application.query.get(id)
    dep_app = Application.query.get(dependency_id)
    if app.remove_dependent_app(dep_app):
        db.session.commit()
        return (
            jsonify({"success": True, "message": "dependency removed"}),
            200,
        )

    return jsonify({"success": False, "message": "dependency does not exist."}), 400
