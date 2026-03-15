from .Authentication import auth_router

ROUTERS = [
    auth_router,
]

__all__ = [
    "auth_router",
    "ROUTERS",
]
