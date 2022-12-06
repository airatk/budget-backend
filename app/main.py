from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import (
    account_controller,
    authentication_controller,
    budget_controller,
    category_controller,
    family_controller,
    transaction_controller,
    user_controller
)
from app.utilities.cors import (
    ALLOWED_HEADERS,
    ALLOWED_METHODS,
    ALLOWED_ORIGINS
)


api: FastAPI = FastAPI(
    title="Budget API",
    description="web API for managing & planning both of joint & personal budgets",
    version="1.0.0",
    contact={
        "name": "Airat K",
        "url": "https://github.com/airatk"
    },
    swagger_ui_parameters={
        "filter": True
    }
)

api.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
    allow_credentials=True
)

api.include_router(authentication_controller)
api.include_router(family_controller)
api.include_router(user_controller)
api.include_router(account_controller)
api.include_router(category_controller)
api.include_router(transaction_controller)
api.include_router(budget_controller)
