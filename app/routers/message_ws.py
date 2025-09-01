#websocket message router

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.operations import message as message_ops
from app.schemas.messages import MessageCreate
from app.models.user import User, UserRole
from app.models.ticket import Ticket
from app.models.message import Message
from fastapi import WebSocket, status
from jose import JWTError, jwt
from app.core import security

#http exception
from fastapi import HTTPException

from app.dependencies import get_current_user, get_current_agent, get_current_admin

from fastapi import WebSocket

router = APIRouter(prefix="/messages", tags=["Messages"])

#load all messages for ticket_id 

@router.get("/{ticket_id}")
def get_messages(ticket_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    #only creator, agent (if assigned), admin can access    
    if current_user.role == UserRole.user and ticket.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this ticket.")
    if current_user.role == UserRole.agent and ticket.agent_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this ticket.")
    if current_user.role == UserRole.admin:
        return message_ops.get_old_messages_for_ticket_id(db, ticket.id)
    return message_ops.get_old_messages_for_ticket_id(db, ticket.id)


# @router.websocket("/{ticket_id}")
# async def websocket_endpoint(websocket: WebSocket, ticket_id: int, message_data: MessageCreate, db: Session = Depends(get_db), ):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
       
#         await websocket.send_text(f"Message text was: {data}")  


@router.websocket("/{ticket_id}")
async def websocket_endpoint(websocket: WebSocket, ticket_id: int, db: Session = Depends(get_db)):
    await websocket.accept()

    # Get token from query params or headers
    token = websocket.query_params.get("token")
    if not token:
        print("No token provided")
        await websocket.close(code=1008)
        return

    # Use your existing token verification logic
    try:
        payload = security.decode_access_token(token)
        user_id: int | None = payload.get("sub")
        if user_id is None:
            print("Invalid token")
            await websocket.close(code=1008)
            return
       
    except JWTError:
        print("Invalid token")

        await websocket.close(code=1008)
        return

    # Get current_user manually (reuse DB + user_id)
    current_user = db.query(User).filter(User.id == user_id).first()
    if not current_user:
        await websocket.close(code=1008)
        return

    # Fetch ticket and check authorization
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    print("Ticket:", ticket.ticket_uid)
    if not ticket:
        print("Ticket not found")
        await websocket.close(code=1008)
        return

    if current_user.role == UserRole.user and ticket.user_id != current_user.id:
        print("User not authorized")
        await websocket.close(code=1008)
        return
    if current_user.role == UserRole.agent and ticket.agent_id != current_user.id:
        print("Agent not authorized")
        await websocket.close(code=1008)
        return
    # Admins pass automatically

    while True:
        try:
            data = await websocket.receive_json()
            message = MessageCreate(**data)

            if message.ticket_id != ticket.id:
                print("Ticket ID mismatch")
                await websocket.close(code=1008)
                return

            new_message = Message(
                ticket_id=message.ticket_id,
                content=message.content,
                sender_id=current_user.id,
                )
            #ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False)
            #sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
            #content = Column(Text, nullable=False)
            db.add(new_message)
            db.commit()
            db.refresh(new_message)
            #send message, sender name, sender id, for ticket
            await websocket.send_json({"message": new_message.content, "sender_name": current_user.name, "sender_id": current_user.id})
        except Exception as e:
            print("WebSocket error:", e)
            await websocket.close(code=1011)
            break
