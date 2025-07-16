from sqlalchemy.orm import Session
from app.models.models import TicketCategory
from app.schemas.ticket_categories import TicketCategoryCreate, TicketCategoryUpdate
from app.utils.responses import ResponseHandler


class TicketCategoryService:
    @staticmethod
    def get_all_ticket_categories(db: Session, page: int, limit: int, search: str = ""):
        ticket_categories = db.query(TicketCategory).order_by(TicketCategory.id.asc()).filter(
            TicketCategory.name.contains(search)).limit(limit).offset((page - 1) * limit).all()
        return {"message": f"Page {page} with {limit} ticket categories", "data": ticket_categories}

    @staticmethod
    def get_ticket_category(db: Session, ticket_category_id: int):
        ticket_category = db.query(TicketCategory).filter(TicketCategory.id == ticket_category_id).first()
        if not ticket_category:
            ResponseHandler.not_found_error("TicketCategory", ticket_category_id)
        return ResponseHandler.get_single_success(ticket_category.name, ticket_category_id, ticket_category)

    @staticmethod
    def create_ticket_category(db: Session, ticket_category: TicketCategoryCreate):
        ticket_category_dict = ticket_category.model_dump()
        db_ticket_category = TicketCategory(**ticket_category_dict)
        db.add(db_ticket_category)
        db.commit()
        db.refresh(db_ticket_category)
        return ResponseHandler.create_success(db_ticket_category.name, db_ticket_category.id, db_ticket_category)

    @staticmethod
    def update_ticket_category(db: Session, ticket_category_id: int, updated_ticket_category: TicketCategoryUpdate):
        db_ticket_category = db.query(TicketCategory).filter(TicketCategory.id == ticket_category_id).first()
        if not db_ticket_category:
            ResponseHandler.not_found_error("TicketCategory", ticket_category_id)

        for key, value in updated_ticket_category.model_dump().items():
            setattr(db_ticket_category, key, value)

        db.commit()
        db.refresh(db_ticket_category)
        return ResponseHandler.update_success(db_ticket_category.name, db_ticket_category.id, db_ticket_category)

    @staticmethod
    def delete_ticket_category(db: Session, ticket_category_id: int):
        db_ticket_category = db.query(TicketCategory).filter(TicketCategory.id == ticket_category_id).first()
        if not db_ticket_category:
            ResponseHandler.not_found_error("TicketCategory", ticket_category_id)
        db.delete(db_ticket_category)
        db.commit()
        return ResponseHandler.delete_success(db_ticket_category.name, db_ticket_category.id, db_ticket_category)
