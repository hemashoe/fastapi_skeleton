import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter

from src.api.api_v1.users_api import user_router
from src.api.api_v1.login_api import login_router

app = FastAPI(title="TEST")
main_router = APIRouter()


main_router.include_router(user_router, prefix="/user", tags=["user"])
main_router.include_router(login_router, prefix="/login", tags=["login"])
app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
