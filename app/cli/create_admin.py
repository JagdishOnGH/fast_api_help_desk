import click
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import user
from app.core.security import get_password_hash

@click.command()
@click.option("--email", prompt=True)
@click.option("--name", prompt=True)
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
def create_admin(email, name, password):
    db: Session = SessionLocal()
    hashed = get_password_hash(password)
    admin = user.User(name=name, email=email, password_hash=hashed, role=user.UserRole.admin)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    print(f"Admin {admin.email} created with ID {admin.id}")

if __name__ == "__main__":
    create_admin()
