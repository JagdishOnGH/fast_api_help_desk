from typing import Union

from fastapi import FastAPI

from app.routers import user
from app.database import Base, engine
from app.auth import router as auth
from app.routers import ticket
from app.routers import ticket_transfer
from app.routers import category
from app.core.seed_category import seed_categories

# Create all tables (development only)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    description="My FastAPI project with Swagger",
    version="1.0.0",
    docs_url="/swagger",       # change Swagger URL
    redoc_url="/redoc"

)
@app.on_event("startup")
def on_startup():
    seed_categories()


app.include_router(user.router)
app.include_router(auth)
app.include_router(ticket.router)
app.include_router(ticket_transfer.router)
app.include_router(category.router)

