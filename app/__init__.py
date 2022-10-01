from fastapi import FastAPI

from app.controllers import authentication_controller
from app.controllers import family_controller
from app.controllers import user_controller
from app.controllers import accounts_controller
from app.controllers import categories_controller
from app.controllers import transactions_controller
from app.controllers import budgets_controller

from app.models.meta import BaseModel

from app.utilities.database import engine


BaseModel.metadata.create_all(bind=engine)

api: FastAPI = FastAPI(
    title="Budget API",
    description="web API for managing & planning both of joint & personal budgets",
    version="1.0.0",
    contact={
        "name": "Airat K",
        "url": "https://github.com/airatk"
    }
)

api.include_router(authentication_controller, tags=[ "authentication" ])
api.include_router(family_controller, tags=[ "family" ])
api.include_router(user_controller, tags=[ "user" ])
api.include_router(accounts_controller, tags=[ "accounts" ])
api.include_router(categories_controller, tags=[ "categories" ])
api.include_router(transactions_controller, tags=[ "transactions" ])
api.include_router(budgets_controller, tags=[ "budgets" ])
