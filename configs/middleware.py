# configs/middleware.py

from fastapi.middleware.cors import CORSMiddleware
from .config import CORS_ORIGINS


def cors_setup(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        # TODO: Restrict allowed_method and allow_headers before shipping to production.
        allow_methods=["*"],
        allow_headers=["*"],
    )
