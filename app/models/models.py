from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float, ARRAY, Enum
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)

    # New column for role
    role = Column(Enum("admin", "user", name="user_roles"), nullable=False, server_default="user")

    # Relationship with carts
    carts = relationship("Cart", back_populates="user")


class TicketOrder(Base):
    __tablename__ = "ticket_orders"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)
    # Relationship with user
    user = relationship("User", back_populates="ticket_orders")

    # Relationship with ticket order items
    ticket_order_items = relationship("TicketOrderItem", back_populates="ticket_order")


class TicketOrderItem(Base):
    __tablename__ = "ticket_order_items"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    ticket_order_id = Column(Integer, ForeignKey("ticket_orders.id", ondelete="CASCADE"), nullable=False)
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)

    # Relationship with ticket order and ticket
    ticket_order = relationship("TicketOrder", back_populates="ticket_order_items")
    ticket = relationship("Ticket", back_populates="ticket_order_items")


class TicketCategory(Base):
    __tablename__ = "ticket_categories"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    # Relationship with tickets
    tickets = relationship("Ticket", back_populates="ticket_category")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)

    # Relationship with ticket category
    ticket_category_id = Column(Integer, ForeignKey("ticket_categories.id", ondelete="CASCADE"), nullable=False)
    ticket_category = relationship("TicketCategory", back_populates="tickets")

    # Relationship with ticket order items
    ticket_order_items = relationship("TicketOrderItem", back_populates="ticket")
