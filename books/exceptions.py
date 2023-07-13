class BookAlreadyBorrowed(Exception):
    pass


class BookAlreadyReturned(Exception):
    pass


class BookNotFound(Exception):
    pass


class SessionNotFound(Exception):
    pass


class UserNotFound(Exception):
    pass


class UsernameMismatchError(Exception):
    pass


class BookNotAssignedToUserError(Exception):
    pass


class BookHistoryException(Exception):
    pass


class AlreadyInBookQueue(Exception):
    pass
