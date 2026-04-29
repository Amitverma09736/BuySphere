from fastapi import HTTPException
from app.models.orders import Order
from app.schemas.orders import OrderCreate  
from sqlalchemy.orm import Session

class OrderService:
    def __init__(self, db:Session):
        self.db = db

    def create_roder(self, order_data:OrderCreate):
        new_order = Order(**order_data.model_dump())
        try:
            self.db.add(new_order)
            self.db.commit()
            self.db.refresh(new_order)
        except:
            self.db.rollback()
            raise
        return new_order
    
    def get_order(self, order_id:int):
        order=self.db.query(Order).filter(Order.id==order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    
    def get_orders(self, skip:int=0, limit:int=100):
        order=self.db.query(Order).offset(skip).limit(limit).all() 
        return order
    
    def update_order(self, order_id:int, order_data:OrderCreate):
        order=self.get_order(order_id)

        for key, value in order_data.model_dump().items():
            setattr(order, key, value)

        try:
            self.db.commit()
            self.db.refresh(order)
        except:
            self.db.rollback()
            raise

        return order

    def delete_order(self, order_id:int):
        order=self.get_order(order_id)
        try:
            self.db.delete(order)
            self.db.commit()
        except:
            self.db.rollback()
            raise