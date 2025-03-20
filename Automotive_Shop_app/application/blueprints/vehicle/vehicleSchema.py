from application.models import Vehicles
from application.extensions import ma

class VehicleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vehicles

vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)