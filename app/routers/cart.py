from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.cart import CartItemCreate, CartItemResponse
from app.crud import cart as crud_cart
from app.core.db import get_db
from app.dependencies.user import get_current_user_id

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/", response_model=list[CartItemResponse])
def read_cart_items(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    items = crud_cart.get_cart_items(db, user_id)
    return [
        CartItemResponse(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            product_name=item.product.name
        )
        for item in items
    ]

@router.post("/", response_model=CartItemResponse)
def add_item_to_cart(cart_item: CartItemCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    item = crud_cart.add_to_cart(db, user_id, cart_item.product_id, cart_item.quantity)
    return CartItemResponse(
        id=item.id,
        product_id=item.product_id,
        quantity=item.quantity,
        product_name=item.product.name
    )

@router.put("/{cart_item_id}", response_model=CartItemResponse)
def update_item_quantity(
    cart_item_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),  
):
    item = crud_cart.update_cart_item(db, user_id, cart_item_id, quantity)  
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return CartItemResponse(
        id=item.id,
        product_id=item.product_id,
        quantity=item.quantity,
        product_name=item.product.name
    )

@router.delete("/{cart_item_id}", response_model=dict)
def delete_cart_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),  
):
    item = crud_cart.remove_cart_item(db, user_id, cart_item_id)  
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"detail": "Cart item removed"}

@router.delete("/clear", response_model=dict)
def clear_user_cart(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    crud_cart.clear_cart(db, user_id)
    return {"detail": "Cart cleared successfully"}
