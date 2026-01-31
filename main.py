# ./main.py

from fastapi import FastAPI
from configs.middleware import cors_setup
from router.Authentication import auth
from router.User import user

app = FastAPI()
cors_setup(app)
app.include_router(auth)
app.include_router(user)


@app.get("/health")
async def health():
    return {"status": "Server is online."}
