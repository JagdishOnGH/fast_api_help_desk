
from app.models.message import Message
from sqlalchemy.orm import Session
from app.schemas.messages import MessageCreate

# get old messages for ticket_id 
def get_old_messages_for_ticket_id(db: Session, ticket_id: int):
    return db.query(Message).filter(Message.ticket_id == ticket_id).all()

# create message
def create_message(db: Session, message_data: MessageCreate):
    db_message = Message(**message_data.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

