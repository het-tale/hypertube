class UserNotFoundException(Exception):
    """Exception raised when a user is not found."""
    pass

class EmailAlreadyInUse(Exception):
    """Exception raised when an entered email already exist"""
    pass

class UsernameAlreadyInUse(Exception):
    """ Excption raised when a username is already in use"""
    pass