from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from app.schemas.tickets import TicketBase
from app.schemas.ticket_categories import TicketCategoryBase


# Base Config
class BaseConfig:
    from_attributes = True


class TicketBaseOrder(TicketBase):
    ticket_category: TicketCategoryBase = Field(exclude=True)

    class Config(BaseConfig):
        pass


# Base TicketOrder & TicketOrderItem
class TicketOrderItemBase(BaseModel):
    id: int
    ticket_id: int
    quantity: int
    subtotal: float
    ticket: TicketBaseOrder


class TicketOrderBase(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    total_amount: float
    ticket_order_items: List[TicketOrderItemBase]

    class Config(BaseConfig):
        pass


class TicketOrderOutBase(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    total_amount: float
    ticket_order_items: List[TicketOrderItemBase]

    class Config(BaseConfig):
        pass


# Get TicketOrder
class TicketOrderOut(BaseModel):
    message: str
    data: TicketOrderBase

    class Config(BaseConfig):
        pass


class TicketOrdersOutList(BaseModel):
    message: str
    data: List[TicketOrderBase]


class TicketOrdersUserOutList(BaseModel):
    message: str
    data: List[TicketOrderBase]

    class Config(BaseConfig):
        pass


# Delete TicketOrder
class TicketOrderOutDelete(BaseModel):
    message: str
    data: TicketOrderOutBase


# Create TicketOrder
class TicketOrderItemCreate(BaseModel):
    ticket_id: int
    quantity: int


class TicketOrderCreate(BaseModel):
    ticket_order_items: List[TicketOrderItemCreate]

    class Config(BaseConfig):
        pass


# Update TicketOrder
class TicketOrderUpdate(TicketOrderCreate):
    pass
