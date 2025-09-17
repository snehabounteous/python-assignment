from app.core.db import engine, Base

from app.models.product import Product
from app.models.cart import CartItem
from app.models.order import Order, OrderItem  
from app.models.user import User

def main():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

if __name__ == "__main__":
    main()
