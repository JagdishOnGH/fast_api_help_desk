from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import Null
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.dependencies import get_current_user # Assuming you have a general get_current_user
from app.operations import ticket as ticket_ops
from app.schemas import ticket as ticket_schema
from app.schemas import ticket_transfer as ticket_transfer_schema
from app.models import user as user_model
from app.models.user import UserRole
from app.models.category import Category
from app.models.subcategory import Subcategory
from app.models.ticket_transfer import TicketTransfer, TransferStatus
from app.models.ticket import TicketPriority, TicketStatus

from datetime import datetime
router = APIRouter(prefix="/tickets_transfers", tags=["Tickets Transfers"])

@router.post("/{ticket_id}/transfer", status_code=status.HTTP_202_ACCEPTED)
def request_ticket_transfer(
    ticket_id: int,
    transfer_request: ticket_schema.TicketTransferRequestCreate,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    """Allows an assigned agent to request a ticket transfer."""

    db_ticket = ticket_ops.get_ticket(db, ticket_id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    #if agent is null and role is admin allow admin to initiate transfer
    if db_ticket.agent_id == None and current_user.role == UserRole.admin:
        return ticket_ops.create_ticket_transfer_request(db, db_ticket=db_ticket, from_agent_id=current_user.id, to_agent_id=transfer_request.to_agent_id, reason=transfer_request.reason)
    
    if current_user.role != UserRole.agent:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only agents can transfer tickets")


    if db_ticket.agent_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to transfer this ticket")

    # Check if the target user is an agent
    target_agent = db.query(user_model.User).filter(user_model.User.id == transfer_request.to_agent_id).first()
    if not target_agent or target_agent.role != UserRole.agent:
        raise HTTPException(status_code=404, detail="Target agent not found or is not an agent")

    ticket_ops.create_ticket_transfer_request(
        db=db,
        db_ticket=db_ticket,
        from_agent_id=current_user.id,
        to_agent_id=transfer_request.to_agent_id,
        reason=transfer_request.reason
    )
    return {"message": "Ticket transfer request submitted for admin approval."}


@router.post("/{transfer_request_id}/transfer/approve", status_code=status.HTTP_202_ACCEPTED)
def approve_ticket_transfer(
        transfer_request_id: int,
        db: Session = Depends(get_db),
        
        current_user: user_model.User = Depends(get_current_user)
    ):
    """Allows an admin to approve a ticket transfer request."""
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can approve ticket transfers")

    db_ticket = ticket_ops.get_transfer_request(db, transfer_request_id)
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket Transfer Request not found")

    if db_ticket.status != TransferStatus.pending:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ticket transfer request is not pending approval")
    
    db_ticket.status = TransferStatus.approved
    db_ticket.resolved_by_admin_id = current_user.id
    db_ticket.resolved_at = datetime.now()

    ticket_ops.approve_ticket_transfer(db, db_ticket)
    return {"message": "Ticket transfer request approved."}


#show all ticket transfer request to admins
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ticket_transfer_schema.TicketTransferRequest] )
def get_transfer_requests(db: Session= Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    """Allows an admin to view all ticket transfer requests."""
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can view ticket transfer requests")
    return ticket_ops.get_transfer_requests(db)
    
    