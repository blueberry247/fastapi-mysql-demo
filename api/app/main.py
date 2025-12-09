from fastapi import FastAPI

from app.db.session import Base, engine
from app.api import items

# Create tables at startup (simple for lab)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI + MySQL Demo (CRUD)")


# Include the items router
app.include_router(items.router)

