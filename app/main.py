from fastapi import FastAPI
from app.routes import homePage, user
from app.routes import category
from app.routes import product
from app.routes import news
from app.routes import our_journey
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Makan Backend")

app.include_router(user.router, prefix="/api", tags=["Users"])
app.include_router(category.router, prefix="/api", tags=["Categories"])
app.include_router(product.router, prefix="/api", tags=["Products"])
app.include_router(news.router, prefix="/api", tags=["News"])
app.include_router(our_journey.router, prefix="/api", tags=["Our Journey"])
app.include_router(homePage.router, prefix="/api", tags=["Home Page"])
app.mount("/app/static", StaticFiles(directory="app/static"), name="static")

# List of allowed origins
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://192.168.1.182:8080",
    "http://192.168.64.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # or ["*"] to allow all origins (not recommended in prod)
    allow_credentials=True,
    allow_methods=["*"],            # allow all methods: GET, POST, PUT, DELETE...
    allow_headers=["*"],            # allow all headers
)

