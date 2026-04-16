from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.products import ProductCreate, ProductResponse
from app.services.product_service import ProductService
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])


# CREATE
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    return product_service.create_product(product)


# GET ALL
@router.get("/", response_model=List[ProductResponse])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    return product_service.get_products(skip, limit)


# GET ONE
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    return product_service.get_product(product_id)


# UPDATE
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_update: ProductCreate, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    return product_service.update_product(product_id, product_update)


# DELETE
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    product_service.delete_product(product_id)
    return None