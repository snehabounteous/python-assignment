from sqlalchemy.orm import Session
from app.models import Order, OrderItem, Product
from app.crud.cart import get_cart_items as get_cart_items_for_user, clear_cart
from fastapi import HTTPException

def create_order(db: Session, user_id: int, total_amount: float) -> Order:
    order = Order(user_id=user_id, total_amount=total_amount, status="pending")
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def add_order_item(db: Session, order_id: int, product_id: int, quantity: int, price: float):
    order_item = OrderItem(
        order_id=order_id,
        product_id=product_id,
        quantity=quantity,
        price_at_time=price
    )
    db.add(order_item)
    db.commit()

def get_product_by_id(db: Session, product_id: int) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def update_product_stock(db: Session, product_id: int, quantity_change: int):
    product = get_product_by_id(db, product_id)
    new_stock = product.stock + quantity_change
    if new_stock < 0:
        raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")
    product.stock = new_stock
    db.commit()

def get_orders_for_user(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()

def get_order_by_id(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
