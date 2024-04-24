

class DoesNotExist(Exception):
    pass


class AuthenticationError(Exception):
    pass


class ValidationError(Exception):
    pass


class LimitExceededError(Exception):
    pass


class AccountBlockedError(Exception):
    pass
