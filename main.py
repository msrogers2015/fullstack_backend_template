# ./main.py

from fastapi import FastAPI
from configs.middleware import cors_setup
from router.Authentication import auth

app = FastAPI()
cors_setup(app)
app.include_router(auth, prefix="/auth", tags=["auth"])


@app.get("/health")
async def health():
    return {"status": "Server is online."}
