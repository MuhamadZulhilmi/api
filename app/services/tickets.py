from sqlalchemy.orm import Session
from app.models.models import Ticket, TicketCategory
from app.schemas.tickets import TicketCreate, TicketUpdate
from app.utils.responses import ResponseHandler


class TicketService:
    @staticmethod
    def get_all_tickets(db: Session, page: int, limit: int, search: str = ""):
        tickets = db.query(Ticket).order_by(Ticket.id.asc()).filter(
            Ticket.title.contains(search)).limit(limit).offset((page - 1) * limit).all()
        return {"message": f"Page {page} with {limit} tickets", "data": tickets}

    @staticmethod
    def get_ticket(db: Session, ticket_id: int):
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            ResponseHandler.not_found_error("Ticket", ticket_id)
        return ResponseHandler.get_single_success(ticket.title, ticket_id, ticket)

    @staticmethod
    def create_ticket(db: Session, ticket: TicketCreate):
        category_exists = db.query(TicketCategory).filter(TicketCategory.id == ticket.ticket_category_id).first()
        if not category_exists:
            ResponseHandler.not_found_error("TicketCategory", ticket.ticket_category_id)

        ticket_dict = ticket.model_dump()
        db_ticket = Ticket(**ticket_dict)
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)
        return ResponseHandler.create_success(db_ticket.title, db_ticket.id, db_ticket)

    @staticmethod
    def update_ticket(db: Session, ticket_id: int, updated_ticket: TicketUpdate):
        db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not db_ticket:
            ResponseHandler.not_found_error("Ticket", ticket_id)

        for key, value in updated_ticket.model_dump().items():
            setattr(db_ticket, key, value)

        db.commit()
        db.refresh(db_ticket)
        return ResponseHandler.update_success(db_ticket.title, db_ticket.id, db_ticket)

    @staticmethod
    def delete_ticket(db: Session, ticket_id: int):
        db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not db_ticket:
            ResponseHandler.not_found_error("Ticket", ticket_id)
        db.delete(db_ticket)
        db.commit()
        return ResponseHandler.delete_success(db_ticket.title, db_ticket.id, db_ticket)
