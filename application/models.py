from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from flask_sqlalchemy import SQLAlchemy
from typing import List


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

inventory_service_tix = db.Table(
    "inventory_service_tix", Base.metadata,
    db.Column("consumable_id", db.ForeignKey("consumable.id")),
    db.Column("ticket_id", db.ForeignKey("service_ticket.ticket_id"))
)

mechanic_service_tix = db.Table(
    "mechanic_service_tix", Base.metadata,
    db.Column("mechanic_id", db.ForeignKey("mechanic.id"), primary_key=True),
    db.Column("ticket_id", db.ForeignKey("service_ticket.ticket_id"), primary_key=True)
)

class Vehicles(Base):
    __tablename__ = "vehicle"

    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(db.String(17), unique=True)
    customer_phone: Mapped[str] = mapped_column(db.String(11), db.ForeignKey("customer.phone_number"), name="fk_vehicle_customer_phone", nullable=True)

    customer: Mapped["Customers"] = relationship("Customers", back_populates="vehicles",foreign_keys=[customer_phone], cascade="all, delete")
    service_tickets: Mapped[List["Service_Tickets"]] = relationship("Service_Tickets", back_populates="vehicle", cascade="all, delete")

class Customers(Base):
    __tablename__ = "customer"

    phone_number: Mapped[str] = mapped_column(db.String(11), primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(db.String(100))
    password: Mapped[str] = mapped_column(db.String(25))
    email: Mapped[str] = mapped_column(db.String(100), unique=True)

    service_tickets: Mapped[List["Service_Tickets"]] = relationship("Service_Tickets", back_populates = "customer")
    vehicles: Mapped[List["Vehicles"]] = relationship("Vehicles", back_populates = "customer", foreign_keys = [Vehicles.customer_phone], cascade="all, delete")

class Mechanics(Base):
    __tablename__ = "mechanic"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[str] = mapped_column(db.String(11))
    name: Mapped[str] = mapped_column(db.String(100))
    skill_level:  Mapped[str] = mapped_column(db.String(7))
    hourly_rate: Mapped[int]
    email: Mapped[str] = mapped_column(db.String(100), unique=True)
    password: Mapped[str] = mapped_column(db.String(25))

    service_tickets: Mapped[List["Service_Tickets"]] = relationship(
        "Service_Tickets",
        secondary=mechanic_service_tix,
        back_populates="mechanics"
    )

class Service_Tickets(Base):
    __tablename__ = "service_ticket"

    ticket_id: Mapped[int] = mapped_column(primary_key=True)
    customer_phone: Mapped[str] = mapped_column(db.String(11), db.ForeignKey("customer.phone_number"))
    vin: Mapped[str] = mapped_column(db.ForeignKey("vehicle.vin"), nullable=True)
    services: Mapped[str] = mapped_column(db.String(10000))
    
    mechanics: Mapped[List["Mechanics"]] = relationship(
        "Mechanics",
        secondary=mechanic_service_tix,
        back_populates="service_tickets"
    )
    
    customer: Mapped["Customers"] = relationship("Customers", back_populates = "service_tickets")
    vehicle: Mapped["Vehicles"] = relationship("Vehicles", back_populates = "service_tickets", foreign_keys=[vin])
    consumables: Mapped["Inventory"] = relationship("Inventory", secondary = inventory_service_tix, back_populates = "service_tickets", cascade="all, delete")

class Inventory(Base):
    __tablename__ = "consumable"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(1000))
    price: Mapped[float] = mapped_column()

    service_tickets: Mapped[List["Service_Tickets"]] = relationship("Service_Tickets", secondary=inventory_service_tix, back_populates = "consumables", cascade="all, delete")



