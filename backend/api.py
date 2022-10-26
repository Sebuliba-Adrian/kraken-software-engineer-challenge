import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


@app.route("/api/test", methods=["GET"])
def testing():
    return jsonify({"status": "success", "message": "testing!"})
