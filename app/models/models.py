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
    role = Column(Enum("admin", "user", "analyst", "cloudflare", "hod", "firewall", name="user_roles"), nullable=False, server_default="user")
    
    # OTP fields
    otp_enabled = Column(Boolean, server_default="False", nullable=False)
    otp_verified = Column(Boolean, server_default="False", nullable=False)
    otp_base32 = Column(String(32), nullable=True)
    otp_auth_url = Column(String(500), nullable=True)

    # Relationship with ticket orders
    ticket_orders = relationship("TicketOrder", back_populates="user")


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
    # Removed ticket relationship to Ticket model to fix mapper error
    # ticket = relationship("Ticket", back_populates="ticket_order_items")


class TicketCategory(Base):
    __tablename__ = "ticket_categories"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    # Removed relationship with tickets due to missing foreign key in Ticket model
    # tickets = relationship("Ticket", back_populates="ticket_category")


from sqlalchemy import func, DateTime

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    title = Column(String(150))
    description = Column(String(250))
    status = Column(String(100))
    customer = Column(String(200))
    agent_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    agent = relationship("User")
    created_date = Column(DateTime, default=func.now(), nullable=False)
    agent_notes = Column(String(1000))
