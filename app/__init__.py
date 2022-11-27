from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import authentication_controller
from app.controllers import family_controller
from app.controllers import users_controller
from app.controllers import accounts_controller
from app.controllers import categories_controller
from app.controllers import transactions_controller
from app.controllers import budgets_controller

from app.utilities.cors import ALLOWED_ORIGINS
from app.utilities.cors import ALLOWED_METHODS
from app.utilities.cors import ALLOWED_HEADERS


api: FastAPI = FastAPI(
    title="Budget API",
    description="web API for managing & planning both of joint & personal budgets",
    version="1.0.0",
    contact={
        "name": "Airat K",
        "url": "https://github.com/airatk"
    }
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
    allow_credentials=True
)

api.include_router(authentication_controller, tags=[ "authentication" ])
api.include_router(family_controller, tags=[ "family" ])
api.include_router(users_controller, tags=[ "user" ])
api.include_router(accounts_controller, tags=[ "accounts" ])
api.include_router(categories_controller, tags=[ "categories" ])
api.include_router(transactions_controller, tags=[ "transactions" ])
api.include_router(budgets_controller, tags=[ "budgets" ])
