from fastapi import FastAPI

from app.database import Base, engine
from app.routes import transaction_routes, analytics_routes

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


# ✅ ROOT API (NO MORE 404)
@app.get("/")
def home():
    return {"message": "Finance Tracker API is running"}


# include routes
app.include_router(transaction_routes.router)
app.include_router(analytics_routes.router)
