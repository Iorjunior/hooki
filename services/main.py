from flask import Blueprint, jsonify, current_app, request


main_blueprint = Blueprint('main', __name__)


@main_blueprint.route("/", methods=['GET'])
def main():
    return jsonify({'status': 'ok'}), 200
