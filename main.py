# ./main.py

from fastapi import FastAPI
from configs.middleware import cors_setup
from router import ROUTERS

app = FastAPI()
cors_setup(app)

for routers in ROUTERS:
    app.include_router(routers)


@app.get("/health")
async def health():
    return {"status": "Server is online."}
