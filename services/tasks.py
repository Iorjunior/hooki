import subprocess
import os

from flask import Blueprint, jsonify, current_app, request
from flask_login import login_required
from datetime import datetime
from threading import Thread

from models.models import Task
from models.serializers import TaskSchema
from utils.hash import generate_token
from utils.task import execute_task_background

tasks_blueprint = Blueprint('tasks', __name__)


@tasks_blueprint.route("/", methods=['GET'])
@login_required
def all_tasks():
    query = Task.query.all()
    return TaskSchema(many=True).jsonify(query), 200


@tasks_blueprint.route("/create", methods=['POST'])
@login_required
def create_task():
    json_data = request.get_json()

    if os.path.isfile(f"{json_data['directory']}/{json_data['command']}"):
        json_data['token'] = generate_token()

        task = Task(**json_data)

        current_app.db.session.add(task)
        current_app.db.session.commit()

        query = Task.query.get(task.id)

        return TaskSchema().jsonify(query), 201
    else:
        return jsonify({'Error': "The file does not exist"}), 204


@tasks_blueprint.route("/update/<id>", methods=['POST'])
@login_required
def update_task(id):
    json_data = request.get_json()

    query = Task.query.filter_by(id=id).update(json_data)
    current_app.db.session.commit()

    query = Task.query.get(id)
    return TaskSchema().jsonify(query), 200


@tasks_blueprint.route("/delete/<id>", methods=['GET'])
@login_required
def delete_task(id):
    query = Task.query.filter(Task.id == id).delete()
    current_app.db.session.commit()

    if query >= 1:
        return jsonify({"deleted": True}), 200

    return jsonify({"deleted": False}), 200


@tasks_blueprint.route("/execute/<id>", methods=['POST'])
def execute_task(id):
    task = Task.query.get(id)
    json_data = request.get_json()

    if json_data['token'] == task.token:
        try:
            thread = Thread(target=execute_task_background, args=(task.command, task.directory))
            thread.daemon = True
            thread.start()

            return jsonify({"task":"started"}), 200
        except Exception as e:
            return jsonify({'Error': str(e)}), 200

    return jsonify("Unauthorized"), 401
