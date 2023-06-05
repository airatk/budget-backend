from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    account_router,
    authentication_router,
    budget_router,
    category_router,
    family_router,
    transaction_router,
    trend_router,
    user_router,
)
from app.utilities.security.cors import (
    ALLOWED_HEADERS,
    ALLOWED_METHODS,
    ALLOWED_ORIGINS,
)


api: FastAPI = FastAPI(
    title='Budget API',
    description='web API for managing & planning both of joint & personal budgets',
    version='1.0.0',
    contact={
        'name': 'Airat K',
        'url': 'https://github.com/airatk',
    },
    swagger_ui_parameters={
        'filter': True,
    },
)

api.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
    allow_credentials=True,
)

api.include_router(authentication_router)
api.include_router(family_router)
api.include_router(user_router)
api.include_router(trend_router)
api.include_router(account_router)
api.include_router(category_router)
api.include_router(transaction_router)
api.include_router(budget_router)
