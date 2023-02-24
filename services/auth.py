from flask import Blueprint, jsonify, current_app, request
from flask_login import LoginManager, login_user, logout_user

from models.models import User

login_manager = LoginManager()


def configure(app):
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


auth_blueprint = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_blueprint.route("/login", methods=['GET'])
def login():
    return 200


@auth_blueprint.route("/logout", methods=['GET'])
def logout():
    logout_user()
    return 200
