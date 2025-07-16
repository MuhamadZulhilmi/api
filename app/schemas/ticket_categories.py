from typing import List
from pydantic import BaseModel, Field


class TicketCategoryBase(BaseModel):
    id: int
    name: str


class TicketCategoryCreate(BaseModel):
    name: str


class TicketCategoryUpdate(BaseModel):
    name: str


class TicketCategoryOut(BaseModel):
    message: str
    data: TicketCategoryBase


class TicketCategoriesOut(BaseModel):
    message: str
    data: List[TicketCategoryBase]


class TicketCategoryDelete(BaseModel):
    id: int
    name: str


class TicketCategoryOutDelete(BaseModel):
    message: str
    data: TicketCategoryDelete
