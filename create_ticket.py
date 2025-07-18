from app.db.database import SessionLocal
from app.models.models import Ticket

def create_sample_ticket():
    db = SessionLocal()
    try:
        ticket = Ticket(
            title="New Ticket",
            description="Description for new ticket",
            status="Open",
            customer="Jane Doe",
            agent="Agent Smith",
            agent_notes="Notes for new ticket"
        )
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        print(f"✅ Ticket created with ID: {ticket.id}")
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating ticket: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_ticket()
