from flask import Flask
from flask_migrate import Migrate

from models.models import configure as config_db
from models.serializers import configure as config_ma


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'dasdas'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hooki.db"

    config_db(app)
    config_ma(app)

    Migrate(app, app.db)

    from services.tasks import tasks_blueprint
    app.register_blueprint(tasks_blueprint, url_prefix='/tasks')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
