from fastapi import FastAPI
from app.api import api_router

app = FastAPI(title="Expeditor API AI")

@app.get("/")
def root():
    return {"message": "API is running"}

app.include_router(api_router)