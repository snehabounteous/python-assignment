from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import OrderCreate, OrderOut
from app.core.db import get_db
from app.crud import order as order_crud, cart, product as product_crud
from app.dependencies.user import get_current_user_id



router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/check-out", response_model=OrderOut)
def checkout_order(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)  
):
    cart_items = cart.get_cart_items(db=db, user_id=user_id)
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0
    for item in cart_items:
        product_obj = product_crud.get_product(db, item.product_id)
        if product_obj.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {product_obj.name}")
        total += product_obj.price * item.quantity

    order_obj = order_crud.create_order(db=db, user_id=user_id, total_amount=total)

    for item in cart_items:
        product_obj = product_crud.get_product(db, item.product_id)
        order_crud.add_order_item(
            db=db,
            order_id=order_obj.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product_obj.price
        )
        order_crud.update_product_stock(db=db, product_id=item.product_id, quantity_change=-item.quantity)

    cart.clear_cart(db=db, user_id=user_id)

    db.refresh(order_obj)
    return order_obj
