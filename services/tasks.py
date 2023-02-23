from flask import Blueprint, jsonify, current_app, request

from models.models import Task
from models.serializers import TaskSchema

tasks_blueprint = Blueprint('tasks', __name__)


@tasks_blueprint.route("/", methods=['GET'])
def all_tasks():
    query = Task.query.all()
    return TaskSchema(many=True).jsonify(query), 200


@tasks_blueprint.route("/create", methods=['POST'])
def create_task():
    json_data = request.get_json()
    task = Task(**json_data)

    current_app.db.session.add(task)
    current_app.db.session.commit()
    
    query = Task.query.get(task.id)
    return TaskSchema().jsonify(query), 201 


@tasks_blueprint.route("/update/<id>", methods=['POST'])
def update_task(id):
    json_data = request.get_json()
    
    query = Task.query.filter_by(id=id).update(json_data)
    current_app.db.session.commit()

    query = Task.query.get(id)
    return TaskSchema().jsonify(query), 200

@tasks_blueprint.route("/delete/<id>", methods=['GET'])
def delete_task(id):
    query = Task.query.filter(Task.id == id).delete()
    current_app.db.session.commit()
    
    return TaskSchema().jsonify(query), 200
