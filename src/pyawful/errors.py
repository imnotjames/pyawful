class AwfulError(BaseException): ...


class InvalidLoginCredentials(AwfulError):
    def __init__(self, message: str, attempt_count: int):
        super().__init__(message)
        self.attempt_count = attempt_count


class RequiresAuthorization(AwfulError): ...


class WasLoggedOut(AwfulError): ...
