from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from flask_sqlalchemy import SQLAlchemy
from typing import List


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


class Customers(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[int] 
    name: Mapped[str] = mapped_column(db.String(100))
    vin: Mapped[str] = mapped_column(db.ForeignKey("vehicle.vin"))

    service_tickets: Mapped[List["Service_Tickets"]] = relationship(back_populates = "customer")
    vehicles: Mapped[List["Vehicles"]] = relationship(back_populates = "phone_number")

class Mechanics(Base):
    __tablename__ = "mechanic"

    employee_id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[int]
    name: Mapped[str] = mapped_column(db.String(100))
    skill_level:  Mapped[str] = mapped_column(db.String(7))
    hourly_rate: Mapped[int]
    ticket_id: Mapped[int] = mapped_column(db.ForeignKey("service_ticket.ticket_id")) 

    tickets: Mapped["Service_Tickets"] = relationship(back_populates = "mechanic")

class Service_Tickets(Base):
    __tablename__ = "service_ticket"

    ticket_id: Mapped[int] = mapped_column(primary_key=True)
    customers: Mapped[str] = mapped_column(db.ForeignKey("customers.phone_number"))
    vin: Mapped[str] = mapped_column(db.ForeignKey("vehicle.vin"))
    mechanic_id: Mapped[str] = mapped_column(db.ForeignKey("mechanics.employee_id"))
    services: Mapped[str] = mapped_column(db.String(10000))

    customer: Mapped["Customers"] = relationship(back_populates = "service_tickets")
    mechanic: Mapped["Mechanics"] = relationship(back_populates = "service_tickets")
    vehicle: Mapped["Vehicles"] = relationship(back_populates = "service_tickets")

class Vehicles(Base):
    __tablename__ = "vehicle"

    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(db.String(17))
    customer: Mapped[int] = mapped_column(db.ForeignKey("customers.phone_number"))

