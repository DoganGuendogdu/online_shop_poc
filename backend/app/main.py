from app.routes import payment_routes

from fastapi import FastAPI

app = FastAPI()

app.include_router(payment_routes.router)
