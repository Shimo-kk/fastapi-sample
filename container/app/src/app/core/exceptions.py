class BadRequestError(Exception):
    pass


class ValidationError(Exception):
    pass


class NotFoundError(Exception):
    pass


class AlreadyExistsError(Exception):
    pass


class ConflictError(Exception):
    pass


class SystemError(Exception):
    pass
