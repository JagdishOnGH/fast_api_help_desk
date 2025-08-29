from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.dependencies import get_current_user # Assuming you have a general get_current_user
from app.operations import ticket as ticket_ops
from app.schemas import ticket as ticket_schema
from app.models import user as user_model
from app.models.user import UserRole
from app.models.category import Category
from app.models.subcategory import Subcategory
from app.models.ticket_transfer import TicketTransfer, TransferStatus
from app.models.ticket import TicketPriority, TicketStatus

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.get("/", response_model=List[ticket_schema.Ticket])
def read_tickets_for_user(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    """
    Retrieves tickets based on the user's role:
    - Admin: Sees all tickets.
    - Agent: Sees tickets assigned to them.
    - User: Sees tickets they created.
    """
    if current_user.role == UserRole.admin:
        return ticket_ops.get_tickets(db, skip=skip, limit=limit)
    elif current_user.role == UserRole.agent:
        return ticket_ops.get_tickets(db, agent_id=current_user.id, skip=skip, limit=limit)
    else: # UserRole.user
        return ticket_ops.get_tickets(db, user_id=current_user.id, skip=skip, limit=limit)

#create ticket if jwt is valid under user's id acquired from jwt


@router.patch("/{ticket_id}/status", response_model=ticket_schema.Ticket)
def update_ticket_status(
    ticket_id: int,
    status_update: ticket_schema.TicketUpdateStatus,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    """Allows Creator, Agent, or Admin to change a ticket's status."""
    db_ticket = ticket_ops.get_ticket(db, ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Permission check: User must be admin, assigned agent, or creator
    is_admin = current_user.role == UserRole.admin
    is_assigned_agent = db_ticket.agent_id == current_user.id
    is_creator = db_ticket.user_id == current_user.id

    if not (is_admin or is_assigned_agent or is_creator):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this ticket")

    return ticket_ops.update_ticket_status(db, db_ticket=db_ticket, status=status_update.status)

# @router.post("/{ticket_id}/transfer", status_code=status.HTTP_202_ACCEPTED)
# def request_ticket_transfer(
#     ticket_id: int,
#     transfer_request: ticket_schema.TicketTransferRequestCreate,
#     db: Session = Depends(get_db),
#     current_user: user_model.User = Depends(get_current_user)
# ):
#     """Allows an assigned agent to request a ticket transfer."""

#     db_ticket = ticket_ops.get_ticket(db, ticket_id)
#     if not db_ticket:
#         raise HTTPException(status_code=404, detail="Ticket not found")
    
#     #if agent is null and role is admin allow admin to initiate transfer
#     if db_ticket.agent_id == None and current_user.role == UserRole.admin:
#         return ticket_ops.create_ticket_transfer_request(db, db_ticket=db_ticket, from_agent_id=current_user.id, to_agent_id=transfer_request.to_agent_id, reason=transfer_request.reason)
    
#     if current_user.role != UserRole.agent:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only agents can transfer tickets")


#     if db_ticket.agent_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to transfer this ticket")

#     # Check if the target user is an agent
#     target_agent = db.query(user_model.User).filter(user_model.User.id == transfer_request.to_agent_id).first()
#     if not target_agent or target_agent.role != UserRole.agent:
#         raise HTTPException(status_code=404, detail="Target agent not found or is not an agent")

#     ticket_ops.create_ticket_transfer_request(
#         db=db,
#         db_ticket=db_ticket,
#         from_agent_id=current_user.id,
#         to_agent_id=transfer_request.to_agent_id,
#         reason=transfer_request.reason
#     )
#     return {"message": "Ticket transfer request submitted for admin approval."}


# @router.post("/{transfer_request_id}/transfer/approve", status_code=status.HTTP_202_ACCEPTED)
# def approve_ticket_transfer(
#         transfer_request_id: int,
#         db: Session = Depends(get_db),
        
#         current_user: user_model.User = Depends(get_current_user)
#     ):
#     """Allows an admin to approve a ticket transfer request."""
#     if current_user.role != UserRole.admin:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can approve ticket transfers")

#     db_ticket = ticket_ops.get_transfer_request(db, transfer_request_id)
#     if not db_ticket:
#         raise HTTPException(status_code=404, detail="Ticket Transfer Request not found")

#     if db_ticket.status != TransferStatus.pending:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ticket transfer request is not pending approval")

#     ticket_ops.approve_ticket_transfer(db, db_ticket)
#     return {"message": "Ticket transfer request approved."}


#create ticket  
@router.post("/", response_model=ticket_schema.Ticket)
def create_ticket(
    ticket_data: ticket_schema.TicketCreate,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    """Allows a user to create a new ticket."""
    if not db.query(Category).filter(Category.id == ticket_data.category_id).first():
        raise HTTPException(status_code=404, detail="Category not found")
    
    return ticket_ops.create_ticket(db, ticket_data, current_user.id)
