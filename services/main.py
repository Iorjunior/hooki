from flask import Blueprint, render_template
from flask_login import login_required

from models.models import Task

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route("/", methods=['GET'])
@login_required
def main():
    query = Task.query.all()
    return render_template('index.html', tasks=query)
