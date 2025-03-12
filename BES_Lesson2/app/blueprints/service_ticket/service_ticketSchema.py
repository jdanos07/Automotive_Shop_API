from app.models import Service_Tickets
from app.extensions import ma

class Service_TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Tickets

service_ticket_schema = Service_TicketSchema()
service_tickets_schema = Service_TicketsSchema(many=True)
