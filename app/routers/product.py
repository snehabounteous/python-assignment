from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.crud import product as product_crud
from app.core.db import get_db

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=Product)
def create_new_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    return product_crud.create_product(db=db, product=product_in)

@router.get("/", response_model=List[Product])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return product_crud.get_products(db=db, skip=skip, limit=limit)

@router.get("/filter", response_model=List[Product])
def filter_products(
    name: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    in_stock: Optional[bool] = Query(False),
    db: Session = Depends(get_db)
):
    return product_crud.filter_products(
        db=db,
        name=name,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock
    )

@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = product_crud.get_product(db=db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=Product)
def update_existing_product(product_id: int, product_in: ProductUpdate, db: Session = Depends(get_db)):
    db_product = product_crud.get_product(db=db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_crud.update_product(db=db, db_product=db_product, updates=product_in)

@router.delete("/{product_id}", status_code=204)
def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    db_product = product_crud.get_product(db=db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    product_crud.delete_product(db=db, db_product=db_product)
    return None
