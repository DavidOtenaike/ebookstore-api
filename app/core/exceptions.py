class UserNotFoundException(Exception):
    pass

class UnauthorizedException(Exception):
    pass

class InvalidCredentialsException(Exception):
    pass

class PurchaseRequiredException(Exception):
    pass

class UserAlreadyExistsException(Exception):
    pass

class InvalidDetailsException(Exception):
    pass

class InvalidRoleException(Exception):
    pass

class BookNotFoundException(Exception):
    pass

class BookAlreadyExistsException(Exception):
    pass

class ReviewNotFoundException(Exception):
    pass