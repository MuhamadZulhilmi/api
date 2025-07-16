from sqlalchemy.orm import Session
from app.models.models import TicketOrder, TicketOrderItem, Ticket
from app.schemas.ticket_orders import TicketOrderUpdate, TicketOrderCreate
from app.utils.responses import ResponseHandler
from sqlalchemy.orm import joinedload
from app.core.security import get_current_user


class TicketOrderService:
    # Get All Ticket Orders
    @staticmethod
    def get_all_ticket_orders(token, db: Session, page: int, limit: int):
        user_id = get_current_user(token)
        ticket_orders = db.query(TicketOrder).filter(TicketOrder.user_id == user_id).offset((page - 1) * limit).limit(limit).all()
        message = f"Page {page} with {limit} ticket orders"
        return ResponseHandler.success(message, ticket_orders)

    # Get A Ticket Order By ID
    @staticmethod
    def get_ticket_order(token, db: Session, ticket_order_id: int):
        user_id = get_current_user(token)
        ticket_order = db.query(TicketOrder).filter(TicketOrder.id == ticket_order_id, TicketOrder.user_id == user_id).first()
        if not ticket_order:
            ResponseHandler.not_found_error("TicketOrder", ticket_order_id)
        return ResponseHandler.get_single_success("ticket order", ticket_order_id, ticket_order)

    # Create a new Ticket Order
    @staticmethod
    def create_ticket_order(token, db: Session, ticket_order: TicketOrderCreate):
        user_id = get_current_user(token)
        ticket_order_dict = ticket_order.model_dump()

        ticket_order_items_data = ticket_order_dict.pop("ticket_order_items", [])
        ticket_order_items = []
        total_amount = 0
        for item_data in ticket_order_items_data:
            ticket_id = item_data['ticket_id']
            quantity = item_data['quantity']

            ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
            if not ticket:
                return ResponseHandler.not_found_error("Ticket", ticket_id)

            subtotal = quantity * ticket.price
            ticket_order_item = TicketOrderItem(ticket_id=ticket_id, quantity=quantity, subtotal=subtotal)
            # total_amount field removed as per request
            # total_amount += subtotal

            ticket_order_items.append(ticket_order_item)
        ticket_order_db = TicketOrder(ticket_order_items=ticket_order_items, user_id=user_id, **ticket_order_dict)
        db.add(ticket_order_db)
        db.commit()
        db.refresh(ticket_order_db)
        return ResponseHandler.create_success("TicketOrder", ticket_order_db.id, ticket_order_db)

    # Update Ticket Order & TicketOrderItem
    @staticmethod
    def update_ticket_order(token, db: Session, ticket_order_id: int, updated_ticket_order: TicketOrderUpdate):
        user_id = get_current_user(token)

        ticket_order = db.query(TicketOrder).filter(TicketOrder.id == ticket_order_id, TicketOrder.user_id == user_id).first()
        if not ticket_order:
            return ResponseHandler.not_found_error("TicketOrder", ticket_order_id)

        # Delete existing ticket_order_items
        db.query(TicketOrderItem).filter(TicketOrderItem.ticket_order_id == ticket_order_id).delete()

        for item in updated_ticket_order.ticket_order_items:
            ticket_id = item.ticket_id
            quantity = item.quantity

            ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
            if not ticket:
                return ResponseHandler.not_found_error("Ticket", ticket_id)

            subtotal = quantity * ticket.price

            ticket_order_item = TicketOrderItem(
                ticket_order_id=ticket_order_id,
                ticket_id=ticket_id,
                quantity=quantity,
                subtotal=subtotal
            )
            db.add(ticket_order_item)

        ticket_order.total_amount = sum(item.subtotal for item in ticket_order.ticket_order_items)

        db.commit()
        db.refresh(ticket_order)
        return ResponseHandler.update_success("ticket order", ticket_order.id, ticket_order)

    # Delete Both Ticket Order and TicketOrderItems
    @staticmethod
    def delete_ticket_order(token, db: Session, ticket_order_id: int):
        user_id = get_current_user(token)
        ticket_order = (
            db.query(TicketOrder)
            .options(joinedload(TicketOrder.ticket_order_items).joinedload(TicketOrderItem.ticket))
            .filter(TicketOrder.id == ticket_order_id, TicketOrder.user_id == user_id)
            .first()
        )
        if not ticket_order:
            ResponseHandler.not_found_error("TicketOrder", ticket_order_id)

        for ticket_order_item in ticket_order.ticket_order_items:
            db.delete(ticket_order_item)

        db.delete(ticket_order)
        db.commit()
        return ResponseHandler.delete_success("TicketOrder", ticket_order_id, ticket_order)
