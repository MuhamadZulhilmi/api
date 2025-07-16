from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, ClassVar
from app.schemas.ticket_categories import TicketCategoryBase


# Base Models
class BaseConfig:
    from_attributes = True


class TicketBase(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_at: datetime
    ticket_category_id: int
    ticket_category: TicketCategoryBase

    class Config(BaseConfig):
        pass


# Create Ticket
class TicketCreate(TicketBase):
    id: ClassVar[int]
    ticket_category: ClassVar[TicketCategoryBase]

    class Config(BaseConfig):
        pass


# Update Ticket
class TicketUpdate(TicketCreate):
    pass


# Get Tickets
class TicketOut(BaseModel):
    message: str
    data: TicketBase

    class Config(BaseConfig):
        pass


class TicketsOut(BaseModel):
    message: str
    data: List[TicketBase]

    class Config(BaseConfig):
        pass


# Delete Ticket
class TicketDelete(TicketBase):
    ticket_category: ClassVar[TicketCategoryBase]


class TicketOutDelete(BaseModel):
    message: str
    data: TicketDelete
