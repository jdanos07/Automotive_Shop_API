from app.models import Vehicles
from app.extensions import ma

class VehicleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vehicles

vehicle_schema = VehicleSchema()
vehicles_schema = VehiclesSchema(many=True)