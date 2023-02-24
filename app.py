from flask import Flask
from flask_migrate import Migrate

from models.models import configure as config_db
from models.serializers import configure as config_ma
from services.auth import configure as config_auth

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'dasdas'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hooki.db"

    config_db(app)
    config_ma(app)
    config_auth(app)

    Migrate(app, app.db, render_as_batch=True)

    from services.tasks import tasks_blueprint
    app.register_blueprint(tasks_blueprint, url_prefix='/tasks')

    from services.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from services.main import main_blueprint
    app.register_blueprint(main_blueprint)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
