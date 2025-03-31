from application.models import Mechanics
from application.extensions import ma

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanics
        include_fk = True

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)