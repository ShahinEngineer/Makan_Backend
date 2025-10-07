from fastapi import FastAPI
from app.routes import user
from app.routes import category
from fastapi.staticfiles import StaticFiles
app = FastAPI(title="Makan Backend")

app.include_router(user.router, prefix="/api", tags=["Users"])
app.include_router(category.router, prefix="/api", tags=["Categories"])

app.mount("/static", StaticFiles(directory="app/static"), name="static")