from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth import router as auth_router
from src.rfid import routers as rfid_router

import sentry_sdk

from config import setting

sentry_sdk.init(
    dsn=setting.sentry_dsn,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()
origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.auth_route)
app.include_router(rfid_router.rfid_route)


# app.include_router(items.router)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0
