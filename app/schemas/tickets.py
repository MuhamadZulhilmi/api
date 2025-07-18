from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, ClassVar

class BaseConfig:
    from_attributes = True

class TicketBase(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    customer: Optional[str]
    agent: Optional[str]
    created_date: datetime
    agent_notes: Optional[str]

    class Config(BaseConfig):
        pass


# Create Ticket
class TicketCreate(BaseModel):
    title: str
    description: Optional[str]
    status: str
    customer: Optional[str]
    agent: Optional[str]
    agent_notes: Optional[str]

    class Config:
        from_attributes = True 


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
class TicketDelete(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    customer: Optional[str]
    agent: Optional[str]
    created_date: datetime
    agent_notes: Optional[str]

    class Config(BaseConfig):
        pass


class TicketOutDelete(BaseModel):
    message: str
    data: TicketDelete

