class UserAlreadyExist(Exception):
    pass


class ServerError(Exception):
    pass

class InvalidCredentials(Exception):
    pass

class DatabaseError(Exception):
    pass

class HistoryNotFound(Exception):
    pass

class UserNotFound(Exception):
    pass

class AdminAlreadyExist(Exception):
    pass

class SecretDataNotFound(Exception):
    pass

class TokenExpired(Exception):
    pass

class InvalidToken(Exception):
    pass

class DatabaseUrlNotFound(Exception):
    pass