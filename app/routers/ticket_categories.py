from fastapi import APIRouter, Depends, Query, status
from app.db.database import get_db
from app.services.ticket_categories import TicketCategoryService
from sqlalchemy.orm import Session
from app.schemas.ticket_categories import TicketCategoryCreate, TicketCategoryOut, TicketCategoriesOut, TicketCategoryOutDelete, TicketCategoryUpdate
from app.core.security import check_admin_role


router = APIRouter(tags=["TicketCategories"], prefix="/ticket_categories")


# Get All Ticket Categories
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=TicketCategoriesOut)
def get_all_ticket_categories(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str | None = Query("", description="Search based name of ticket categories"),
):
    return TicketCategoryService.get_all_ticket_categories(db, page, limit, search)


# Get Ticket Category By ID
@router.get(
    "/{ticket_category_id}",
    status_code=status.HTTP_200_OK,
    response_model=TicketCategoryOut)
def get_ticket_category(ticket_category_id: int, db: Session = Depends(get_db)):
    return TicketCategoryService.get_ticket_category(db, ticket_category_id)


# Create New Ticket Category
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=TicketCategoryOut,
    dependencies=[Depends(check_admin_role)])
def create_ticket_category(ticket_category: TicketCategoryCreate, db: Session = Depends(get_db)):
    return TicketCategoryService.create_ticket_category(db, ticket_category)


# Update Existing Ticket Category
@router.put(
    "/{ticket_category_id}",
    status_code=status.HTTP_200_OK,
    response_model=TicketCategoryOut,
    dependencies=[Depends(check_admin_role)])
def update_ticket_category(ticket_category_id: int, updated_ticket_category: TicketCategoryUpdate, db: Session = Depends(get_db)):
    return TicketCategoryService.update_ticket_category(db, ticket_category_id, updated_ticket_category)


# Delete Ticket Category By ID
@router.delete(
    "/{ticket_category_id}",
    status_code=status.HTTP_200_OK,
    response_model=TicketCategoryOutDelete,
    dependencies=[Depends(check_admin_role)])
def delete_ticket_category(ticket_category_id: int, db: Session = Depends(get_db)):
    return TicketCategoryService.delete_ticket_category(db, ticket_category_id)
