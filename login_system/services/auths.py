from string import ascii_letters, digits, punctuation
from enum import Enum, unique
from secrets import compare_digest


@unique
class AuthTypes(Enum):
    """ A class of infos for replying auth """
    SUCCESS                  = 1
    FAILED                   = 0
    SHORT_PASSWORD           = 3
    LONG_PASSWORD            = 4
    PASSWORDS_MISMATCH       = 5
    LONG_USERNAME            = 6
    ILLEGAL_START            = 7
    CONTAINS_ILLEGAL_CHARS   = 8
    NOT_AN_INTEGER           = 9
    USERNAME_ALREADY_EXISTS  = 10

""" A module for basic authentictors """



def auth_age(age, genesis) -> AuthTypes:
    """ Authenticates the age seeing to it that it's above genesis """
    if age.isdigit():
        if (age := int(age)) >= genesis:
            return AuthTypes.SUCCESS, age
        return AuthTypes.FAILED, 0
    return AuthTypes.NOT_AN_INTEGER, 0 


def auth_name(name):
    """ Authenticates names with no illegal characters """
    return AuthTypes.SUCCESS if name.isalpha() else AuthTypes.FAILED


def auth_password(password, confirm_password) -> AuthTypes:
    """ 
    Authenticates password matches between password and confirm_password,
    also makes sure it's >= 8:    
    """
    if compare_digest(password, confirm_password):
        if length := len(password) >= 8:
            return AuthTypes.SUCCESS
        elif length > 30:
            return AuthTypes.LONG_PASSWORD
        else:
            return AuthTypes.SHORT_PASSWORD
    else:
        return AuthTypes.PASSWORDS_MISMATCH


def auth_username(username) -> AuthTypes:
    """
    Authenticates the username according to these standards:
       
      * username should not start with any other character apart from the alphabets
      * username should not contain any whitespace character
      * username should can contain any character in [_,.] apart from the alphabets
      * username should not be more than 30 characters long.
    """
    accepted_chars = f"@_.{ascii_letters}{digits}" # chras to accept
    starts = any(tuple(username.startswith(char) for char in digits+punctuation)) # check for illegal start
    contains = any(map(lambda x: x not in accepted_chars, username)) # check if containing illegal chars
    long = len(username) > 15 # check username length

    if not starts:
        if not contains:
            if not long:
                return AuthTypes.SUCCESS
            else:
                return AuthTypes.LONG_USERNAME
        else:
            return AuthTypes.CONTAINS_ILLEGAL_CHARS
    else:
        return AuthTypes.ILLEGAL_START
