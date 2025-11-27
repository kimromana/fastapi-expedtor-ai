from fastapi import FastAPI

app = FastAPI(title="Expeditor API AI")

@app.get("/")
def root():
    return {"message": "API is running"}
