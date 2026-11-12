class AppError(Exception):
    """Base exception for all app errors"""


class NotFoundError(AppError):
    def __init__(self,resource: str, key: str):
        super().__init__(f"'{resource}' not found with key '{key}'")


class ConflictError(AppError):
    def __init__(self,resource: str, key: str):
        super().__init__(f"'{resource}' already exists with key '{key}'")

class LLMUnavailableError(AppError):
    """Raised when LLM is not available"""
    # def __init__(self,resource: str, key: str):
    #     ...

class UnauthorizedError(AppError):
    """Raised when the caller is not logged in, or the token is bad."""
    # def __init__(self,resource: str, key: str):

class ForbiddenError(AppError):
    """Raised when the caller is logged in but not allowed to do this."""