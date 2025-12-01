from fastapi import FastAPI
from app.api import api_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Expeditor API AI")

@app.get("/")
def root():
    return {"message": "API is running"}

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)