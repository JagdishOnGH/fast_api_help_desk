from typing import Union

from fastapi import FastAPI

app = FastAPI(
    description="My FastAPI project with Swagger",
    version="1.0.0",
    docs_url="/swagger",       # change Swagger URL
    redoc_url="/redoc"
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}