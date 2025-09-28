from fastapi import FastAPI

app = FastAPI(title="Makan Backend")

@app.get("/")
async def read_root():
    return {"Hello": "World"}
# --- IGNORE ---