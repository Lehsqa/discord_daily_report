from http import HTTPStatus as status


class BaseError(Exception):
    def __init__(
        self,
        message: str = "",
        status_code: int = status.INTERNAL_SERVER_ERROR,
    ) -> None:
        self.message: str = message
        self.status_code: int = status_code

        super().__init__(message)


class DatabaseError(BaseError):
    def __init__(
        self, message: str = "Database error"
    ) -> None:
        super().__init__(
            message=message, status_code=status.INTERNAL_SERVER_ERROR
        )


class UnprocessableError(BaseError):
    def __init__(
        self, message: str = "Validation error"
    ) -> None:
        super().__init__(
            message=message,
            status_code=status.UNPROCESSABLE_ENTITY,
        )


class NotFoundError(BaseError):
    def __init__(self, message: str = "Not found") -> None:
        super().__init__(
            message=message, status_code=status.NOT_FOUND
        )
