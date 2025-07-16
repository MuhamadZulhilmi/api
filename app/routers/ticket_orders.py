from fastapi import APIRouter, Depends, Query, status
from app.db.database import get_db
from app.services.ticket_orders import TicketOrderService
from sqlalchemy.orm import Session
from app.schemas.ticket_orders import TicketOrderCreate, TicketOrderUpdate, TicketOrderOut, TicketOrderOutDelete, TicketOrdersOutList
from app.core.security import get_current_user
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

router = APIRouter(tags=["TicketOrders"], prefix="/ticket_orders")
auth_scheme = HTTPBearer()


# Get All Ticket Orders
@router.get("/", status_code=status.HTTP_200_OK, response_model=TicketOrdersOutList)
def get_all_ticket_orders(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    return TicketOrderService.get_all_ticket_orders(token, db, page, limit)


# Get Ticket Order By User ID
@router.get("/{ticket_order_id}", status_code=status.HTTP_200_OK, response_model=TicketOrderOut)
def get_ticket_order(
        ticket_order_id: int,
        db: Session = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    return TicketOrderService.get_ticket_order(token, db, ticket_order_id)


# Create New Ticket Order
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TicketOrderOut)
def create_ticket_order(
        ticket_order: TicketOrderCreate, db: Session = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    return TicketOrderService.create_ticket_order(token, db, ticket_order)


# Update Existing Ticket Order
@router.put("/{ticket_order_id}", status_code=status.HTTP_200_OK, response_model=TicketOrderOut)
def update_ticket_order(
        ticket_order_id: int,
        updated_ticket_order: TicketOrderUpdate,
        db: Session = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    return TicketOrderService.update_ticket_order(token, db, ticket_order_id, updated_ticket_order)


# Delete Ticket Order By User ID
@router.delete("/{ticket_order_id}", status_code=status.HTTP_200_OK, response_model=TicketOrderOutDelete)
def delete_ticket_order(
        ticket_order_id: int, db: Session = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    return TicketOrderService.delete_ticket_order(token, db, ticket_order_id)
