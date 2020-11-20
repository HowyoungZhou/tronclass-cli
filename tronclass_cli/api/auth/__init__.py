class AuthProvider:
    desc = None

    def __init__(self):
        pass

    def login(self, *args, **kwargs):
        pass


class AuthError(Exception):
    def __init__(self, message='Failed to authenticate. Please check your user name and password.'):
        super().__init__(message)
