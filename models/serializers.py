from flask_marshmallow import Marshmallow
from models.models import Task

ma = Marshmallow()


def configure(app):
    ma.init_app(app)


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task