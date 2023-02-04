from typing import Optional

__all__ = ["BaseAPIException"]


class BaseAPIException(BaseException):
    # TODO: Добавить описание

    message: Optional[str] = "Base API Exception"

    def __init__(self, message: Optional[str] = None):
        if message is not None:
            self.message = message

        super().__init__(self.message)
