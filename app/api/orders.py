from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.orders import Order
from app.models.products import Product
from app.models.users import User
from app.schemas.orders import OrderCreate, OrderResponse
from typing import List

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/{user_id}", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(user_id: int, order: OrderCreate, db: Session = Depends(get_db)):
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Verify product exists
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    # Check minimum stock
    if product.stock < order.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")
        
    # Calculate total
    total_amount = product.price * order.quantity
    
    # Update stock
    product.stock -= order.quantity
    
    # Create order
    new_order = Order(
        user_id=user_id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_amount=total_amount
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    return new_order

@router.get("/{user_id}", response_model=List[OrderResponse])
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return orders

@router.get("/detail/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
