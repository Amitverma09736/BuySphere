from fastapi import FastAPI
from app.db.database import test_db_connection, Base, engine
from app.models import users, products, orders
from app.api.users import router as users_router
from app.api.products import router as products_router
from app.api.orders import router as orders_router

# Create DB Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce API")

app.include_router(users_router)
app.include_router(products_router)
app.include_router(orders_router)

@app.on_event("startup")
def startup():
    print("🚀 Starting app...")
    test_db_connection()

@app.get("/")
def home():
    return {"message": "Ecommerce API running"}