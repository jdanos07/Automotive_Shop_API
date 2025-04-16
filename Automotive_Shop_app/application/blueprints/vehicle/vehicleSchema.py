from models import Vehicles
from extensions import ma

class VehicleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vehicles
        include_fk = True

vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)