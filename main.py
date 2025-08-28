from typing import Union

from fastapi import FastAPI

from app.routers import user
from app.database import Base, engine
from app.auth import router as auth

# Create all tables (development only)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    description="My FastAPI project with Swagger",
    version="1.0.0",
    docs_url="/swagger",       # change Swagger URL
    redoc_url="/redoc"

)


app.include_router(user.router)
app.include_router(auth)
