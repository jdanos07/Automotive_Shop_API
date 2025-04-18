from application.models import Inventory
from application.extensions import ma

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory

consumable_schema = InventorySchema()
consumables_schema = InventorySchema(many=True)