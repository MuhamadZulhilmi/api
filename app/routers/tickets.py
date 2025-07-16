from fastapi import APIRouter, Depends, Query, status
from app.db.database import get_db
from app.services.tickets import TicketService
from sqlalchemy.orm import Session
from app.schemas.tickets import TicketCreate, TicketOut, TicketsOut, TicketOutDelete, TicketUpdate
from app.core.security import get_current_user, check_admin_role


router = APIRouter(tags=["Tickets"], prefix="/tickets")


# Get All Tickets
@router.get("/", status_code=status.HTTP_200_OK, response_model=TicketsOut)
def get_all_tickets(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str | None = Query("", description="Search based title of tickets"),
):
    return TicketService.get_all_tickets(db, page, limit, search)


# Get Ticket By ID
@router.get("/{ticket_id}", status_code=status.HTTP_200_OK, response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    return TicketService.get_ticket(db, ticket_id)


# Create New Ticket
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=TicketOut,
    dependencies=[Depends(check_admin_role)])
def create_ticket(
        ticket: TicketCreate,
        db: Session = Depends(get_db)):
    return TicketService.create_ticket(db, ticket)


# Update Exist Ticket
@router.put(
    "/{ticket_id}",
    status_code=status.HTTP_200_OK,
    response_model=TicketOut,
    dependencies=[Depends(check_admin_role)])
def update_ticket(
        ticket_id: int,
        updated_ticket: TicketUpdate,
        db: Session = Depends(get_db)):
    return TicketService.update_ticket(db, ticket_id, updated_ticket)


# Delete Ticket By ID
@router.delete(
    "/{ticket_id}",
    status_code=status.HTTP_200_OK,
    response_model=TicketOutDelete,
    dependencies=[Depends(check_admin_role)])
def delete_ticket(
        ticket_id: int,
        db: Session = Depends(get_db)):
    return TicketService.delete_ticket(db, ticket_id)
