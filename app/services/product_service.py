from fastapi import HTTPException
from app.models.products import Product
from app.schemas.products import ProductCreate
from sqlalchemy.orm import Session

class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product_data: ProductCreate):
        new_product = Product(**product_data.model_dump())
        try:
            self.db.add(new_product)
            self.db.commit()
            self.db.refresh(new_product)
        except:
            self.db.rollback()
            raise
        return new_product

    def get_product(self, product_id: int):
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
        
    def get_products(self, skip: int = 0, limit: int = 100):
        return self.db.query(Product).offset(skip).limit(limit).all()

    def update_product(self, product_id: int, product_data: ProductCreate):
        product = self.get_product(product_id)

        for key, value in product_data.model_dump().items():
            setattr(product, key, value)

        try:
            self.db.commit()
            self.db.refresh(product)
        except:
            self.db.rollback()
            raise

        return product

    def delete_product(self, product_id: int):
        product = self.get_product(product_id)

        try:
            self.db.delete(product)
            self.db.commit()
        except:
            self.db.rollback()
            raise