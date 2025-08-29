from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import user as user_model
from app.models.ticket import TicketPriority, TicketStatus
from app.models.ticket_transfer import TicketTransfer, TransferStatus
import random 

from app.models.ticket import Ticket as ticket_model
from app.schemas.ticket import Ticket as ticket_schema, DashboardStats
from app.models.category import Category
from app.models.subcategory import Subcategory
from typing import Optional



def get_ticket(db: Session, ticket_id: int):
    """Gets a single ticket by its ID."""
    return db.query(ticket_model).filter(ticket_model.id == ticket_id).first()

def get_transfer_request(db: Session, ticket_transfer_id: int):
    return db.query(TicketTransfer).filter(ticket_transfer_id == TicketTransfer.id).first()

def get_transfer_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TicketTransfer).offset(skip).limit(limit).all()

def get_tickets(db: Session, user_id: int = None, agent_id: int = None, skip: int = 0, limit: int = 100):
    """
    Gets a list of tickets.
    - If user_id is provided, filters for that user's created tickets.
    - If agent_id is provided, filters for that agent's assigned tickets.
    - If neither is provided, returns all tickets (for admins).
    """
    query = db.query(ticket_model)
    
    if user_id:
        query = query.filter(ticket_model.user_id == user_id)
    
    if agent_id:
        query = query.filter(ticket_model.agent_id == agent_id)
        
    return query.offset(skip).limit(limit).all()

def update_ticket_status(db: Session, db_ticket: ticket_model, status: TicketStatus):
    """Updates the status of a given ticket."""
    db_ticket.status = status
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def get_dashboard_stats(db: Session) -> DashboardStats:
    """Calculates and returns dashboard statistics."""
    total_tickets = db.query(func.count(ticket_model.id)).scalar()
    
    resolved_statuses = [TicketStatus.resolved, TicketStatus.closed]
    resolved_tickets = db.query(func.count(ticket_model.id)).filter(ticket_model.status.in_(resolved_statuses)).scalar()
    
    pending_tickets = total_tickets - resolved_tickets
    
    return DashboardStats(
        total_tickets=total_tickets,
        resolved_tickets=resolved_tickets,
        pending_tickets=pending_tickets
    )
    # Add these imports at the top of app/operations/ticket.py
# Needed for random UID generation

# ... (keep existing functions like get_ticket, get_tickets, etc.) ...

def _generate_ticket_uid() -> str:
    """Generates a simple, user-friendly unique ticket ID."""
    # In a real-world app, you might want a more robust system
    # like combining timestamp and a random component.
    return f"TICKET-{random.randint(100000, 999999)}"

def _score_priority(title: str, description: str) -> TicketPriority:
    """
    ALGORITHM #1: Keyword-Based Priority Scoring.
    Scans ticket content for keywords to automatically set priority.
    """
    content = f"{title.lower()} {description.lower()}"
    
    # Define keywords and their corresponding priorities
    if any(keyword in content for keyword in ['outage', 'critical', 'down', 'urgent', 'broken']):
        return TicketPriority.urgent
    elif any(keyword in content for keyword in ['error', 'fail', 'slow', 'no internet']):
        return TicketPriority.high
    elif any(keyword in content for keyword in ['question', 'inquiry', 'how to', 'request']):
        return TicketPriority.low
    else:
        return TicketPriority.medium # Default priority

def _find_best_agent(db: Session, category_id: int) -> Optional[int]:
    """
    ALGORITHM #2: Least Connections Agent Assignment.
    Finds the agent assigned to the category with the fewest active tickets.
    """
    # Find agents assigned to this category
    assigned_agents_query = db.query(user_model.User.id).join(
        user_model.User.assigned_categories
    ).filter(
        user_model.User.role == user_model.UserRole.agent,
        user_model.User.assigned_categories.any(id=category_id)
    )
    
    assigned_agent_ids = [agent_id for agent_id, in assigned_agents_query.all()]
    
    if not assigned_agent_ids:
        return None # No agent is available for this category

    # Find the agent among them with the minimum number of active tickets
    # Active statuses are 'assigned' and 'in_progress'
    active_statuses = [TicketStatus.assigned, TicketStatus.in_progress]
    
    result = db.query(
        ticket_model.agent_id, 
        func.count(ticket_model.id).label('active_tickets')
    ).filter(
        ticket_model.agent_id.in_(assigned_agent_ids),
        ticket_model.status.in_(active_statuses)
    ).group_by(ticket_model.agent_id).order_by('active_tickets').first()
    
    if result:
        # An agent with active tickets was found, return the one with the least
        return result.agent_id
    else:
        # No agents have active tickets, so just pick one from the available list
        return assigned_agent_ids[0]

def create_ticket(db: Session, ticket_data: ticket_schema, user_id: int):
    """
    Creates a new ticket, scores its priority, and assigns it to the best agent.
    """

    # if category and or sub category are not exist raise error
  
    
    # 1. Score Priority
    priority = _score_priority(ticket_data.title, ticket_data.initial_description)
    
    # 2. Find Best Agent
    best_agent_id = _find_best_agent(db, ticket_data.category_id)
    
    # Determine initial status based on agent availability
    status = TicketStatus.assigned if best_agent_id else TicketStatus.open
    
    # 3. Create Ticket Record
    db_ticket = ticket_model(
        **ticket_data.model_dump(),
        ticket_uid=_generate_ticket_uid(),
        user_id=user_id,
        agent_id=best_agent_id,
        priority=priority,
        status=status,
    )

    
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def create_ticket_transfer_request(db: Session, db_ticket: ticket_model, from_agent_id: int, to_agent_id: int, reason: str):
    """Creates a ticket transfer request record."""
    transfer_request = TicketTransfer(
        ticket_id=db_ticket.id,
        from_agent_id=from_agent_id,
        to_agent_id=to_agent_id,
        request_reason=reason,
        status= TransferStatus.pending
    )
    db.add(transfer_request)
    db.commit()
    db.refresh(transfer_request)
    return transfer_request

def approve_ticket_transfer(db: Session, transfer_request: TicketTransfer):
    db.add
    db.commit()
    db.refresh(transfer_request)
    return transfer_request
