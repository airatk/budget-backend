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


backend: FastAPI = FastAPI(
    title='Budget Backend',
    description='backend for managing & planning both of joint & personal budgets',
    version='1.0.0',
    contact={
        'name': 'Airat K',
        'url': 'https://github.com/airatk',
    },
    swagger_ui_parameters={
        'filter': True,
    },
)

backend.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
    allow_credentials=True,
)

backend.include_router(authentication_router)
backend.include_router(family_router)
backend.include_router(user_router)
backend.include_router(trend_router)
backend.include_router(account_router)
backend.include_router(category_router)
backend.include_router(transaction_router)
backend.include_router(budget_router)
