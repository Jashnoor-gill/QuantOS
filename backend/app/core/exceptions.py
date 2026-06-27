from fastapi import HTTPException


class AuthException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=401,
            detail=detail,
        )

class DatabaseException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=500,
            detail=detail,
        )

class InvalidTokenException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=401,
            detail=detail,
        )