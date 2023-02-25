from flask import Flask
from environs import Env
from flask_migrate import Migrate

from models.models import configure as config_db
from models.serializers import configure as config_ma
from services.auth import configure as config_auth

env = Env()
env.read_env()

SECRET_KEY = env("SECRET_KEY")
URL_PREFIX = env("URL_PREFIX")
DB_URL = env("DB_URL")


def create_app():
    app = Flask(__name__, static_url_path=f'{URL_PREFIX}/static')
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL

    config_db(app)
    config_ma(app)
    config_auth(app)

    Migrate(app, app.db, render_as_batch=True)

    from services.tasks import tasks_blueprint
    app.register_blueprint(tasks_blueprint, url_prefix=f'{URL_PREFIX}/tasks')

    from services.auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix=f'{URL_PREFIX}/')

    from services.main import main_blueprint
    app.register_blueprint(main_blueprint, url_prefix=f'{URL_PREFIX}/')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
