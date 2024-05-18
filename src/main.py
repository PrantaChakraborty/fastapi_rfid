from fastapi import Depends, FastAPI

from src.auth import router

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()


app.include_router(router.auth_route)
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