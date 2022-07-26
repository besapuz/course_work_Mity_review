class BaseServiceError(Exception):
    code = 500


class UserNotFound(BaseServiceError):
    pass


class WrongPassword(BaseServiceError):
    pass


class IncorrectPassword(BaseServiceError):
    pass


class UserAlreadyExists(BaseServiceError):
    pass


class ItemNotFound(BaseServiceError):
    pass

class InvalidToken(BaseServiceError):
    pass
