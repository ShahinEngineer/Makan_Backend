from fastapi import FastAPI
from app.routes import user
app = FastAPI(title="Makan Backend")

app.include_router(user.router, prefix="/api")