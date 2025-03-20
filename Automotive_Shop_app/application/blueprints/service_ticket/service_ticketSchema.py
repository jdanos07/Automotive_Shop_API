from application.models import Service_Tickets
from application.extensions import ma

class Service_TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Tickets

service_ticket_schema = Service_TicketSchema()
service_tickets_schema = Service_TicketSchema(many=True)
