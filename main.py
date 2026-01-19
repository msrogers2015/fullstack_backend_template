from fastapi import FastAPI
from configs.middleware import cors_setup

app = FastAPI()
cors_setup(app)

@app.get('/health')
async def health():
    return {'status': 'Server is online.'}