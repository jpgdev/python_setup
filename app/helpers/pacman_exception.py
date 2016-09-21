from .pacman_error_type import PacmanErrorType


class PacmanException(Exception):
    default_message = 'There was an unknown error with pacman'

    def __init__(self,
                 message=default_message,
                 status_code=0,
                 error_type=PacmanErrorType.unknown,
                 args=[]):
        self.message = message
        self.status_code = status_code
        self.error_type = error_type
        self.args = args

    # def __str__(self):
    #     return self.message
