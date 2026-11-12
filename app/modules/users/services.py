import uuid
from app.modules.users.models import User
from app.modules.users.repositories import UserRepository
from app.modules.users.schemas import CreateUser, ReadUser, Token
from app.core.exceptions.errors import ConflictError, UnauthorizedError
from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password
)

class UserService:
    """Business rules for accounts"""

    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def register(self, data: CreateUser) -> ReadUser:
        email = data.email.lower()
        if await self.repo.get_by_email(email):
            raise ConflictError("User", email)
        user = User(email=email, password=hash_password(data.password))
        return ReadUser.model_validate(await self.repo.add(user))

    async def login(self, email: str, password: str) -> Token:
        user = await self.repo.get_by_email(email.lower())
        if user is None or not verify_password(password, user.password):
            raise UnauthorizedError("Incorrect email or password")
        if not user.is_active:
            raise UnauthorizedError("Account is disabled")
        return Token(access_token=create_access_token(str(user.id)))

    async def get_user_by_token(self, token: str) -> User:
        payload = decode_access_token(token)
        if payload is None:
            raise UnauthorizedError("Invalid or expired token")
        user: User | None = await self.repo.get_by_id(uuid.UUID(payload["sub"]))
        if user is None or not user.is_active:
            raise UnauthorizedError("Invalid or expired token")
        return user