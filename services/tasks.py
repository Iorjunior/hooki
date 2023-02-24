import subprocess

from flask import Blueprint, jsonify, current_app, request
from flask_login import login_required

from models.models import Task
from models.serializers import TaskSchema
from utils.hash import generate_token

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
    json_data['token'] = generate_token()
    
    task = Task(**json_data)

    current_app.db.session.add(task)
    current_app.db.session.commit()

    query = Task.query.get(task.id)
    return TaskSchema().jsonify(query), 201


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

    return TaskSchema().jsonify(query), 200


@tasks_blueprint.route("/execute/<id>", methods=['POST'])
def execute_task(id):
    task = Task.query.get(id)
    json_data = request.get_json()

    if json_data['token'] == task.token:
        process = subprocess.run(f"{task.command}", shell=True, stdout=subprocess.PIPE, cwd=task.directory)
        res = [r for r in str(process.stdout, 'UTF-8').split("\n") if r]

        return jsonify(res)
    
    return jsonify("Unauthorized")

