from fastapi import APIRouter


user_controller: APIRouter = APIRouter(prefix="/user")


@user_controller.get("/authenticate")
async def authenticate():
    pass


@user_controller.get("/current")
async def get_current_user():
    pass
