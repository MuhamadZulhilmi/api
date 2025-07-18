from sqlalchemy.orm import Session
from app.models.models import Ticket
from app.schemas.tickets import TicketCreate, TicketUpdate
from app.utils.responses import ResponseHandler


class TicketService:
    @staticmethod
    def get_ticket(db: Session, ticket_id: int):
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            ResponseHandler.not_found_error("Ticket", ticket_id)
        return ResponseHandler.get_single_success(ticket.title, ticket_id, ticket)

    @staticmethod
    def get_all_tickets(db: Session, page: int = 1, limit: int = 10, search: str = ""):
        query = db.query(Ticket)
        if search:
            query = query.filter(Ticket.title.ilike(f"%{search}%"))
        tickets = query.order_by(Ticket.id.asc()).limit(limit).offset((page - 1) * limit).all()
        return {"message": f"Page {page} with {limit} tickets", "data": tickets}

    @staticmethod
    def create_ticket(db: Session, ticket: TicketCreate):
        db_ticket = Ticket(**ticket.model_dump())
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

