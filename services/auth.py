from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import LoginManager, login_user, logout_user, login_required

from models.models import User
from datetime import timedelta

login_manager = LoginManager()


def configure(app):
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


auth_blueprint = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.verify_password(password):
            login_user(user=user, remember=True, duration=timedelta(days=1))
            return redirect(url_for('main.main'))

        error = True

    return render_template('login.html', error=error)


@auth_blueprint.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
