from app.models import Mechanics
from app.extensions import ma

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanics

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicsSchema(many=True)