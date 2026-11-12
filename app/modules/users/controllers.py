from fastapi import APIRouter, status, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.modules.users.dependencies import UserServiceDep, CurrentUserDep
from app.modules.users.schemas import CreateUser, ReadUser, Token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=ReadUser, status_code=status.HTTP_201_CREATED)
async def register(data: CreateUser, service: UserServiceDep) -> ReadUser:
    return await service.register(data)

@router.post("/login", response_model=Token)
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], service: UserServiceDep) -> Token:
    return await service.login(email=form.username, password=form.password)


@router.get("/me", response_model=ReadUser)
async def me(user: CurrentUserDep) -> ReadUser:
    return ReadUser.model_validate(user)