from fastapi import FastAPI, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routers import product, cart, order, user  

def add_user_id_header(x_user_id: int = Header(default=1)):
    return x_user_id

app = FastAPI(dependencies=[Depends(add_user_id_header)])

app.include_router(product.router)
app.include_router(cart.router)
app.include_router(order.router)
app.include_router(user.router)
