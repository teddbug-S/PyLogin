from enum import Enum, unique

@unique
class InfoTypes(Enum):
    """ Some infos to return 

    :param Enum: Inherits from Enum
    :type Enum: Enum
    """
    # Database info
    DATABASE_NOT_FOUND            =  1
    DATABASE_CLEARED_SUCCESSFULLY =  2
    CREATE_DATABASE_SUCCESSFUL    =  3
    DATABASE_ALREADY_EXISTS       =  4
    DATABASE_SET_SUCCESSFUL       =  5
    DATABASE_NOT_SET              =  6

    # database tables info
    TABLE_ALREADY_EXISTS          =  7
    TABLE_NOT_FOUND               =  8
    TABLE_CREATED_SUCCESSFULLY    =  9

    # Account info
    CREATE_ACCOUNT_SUCCESSFUL     =  10
    ACCOUNT_NOT_FOUND             =  11
    LOGIN_ADMIN_SUCCESSFUL        =  12
    LOGIN_USER_SUCCESSFUL         =  13
    WRONG_PASSWORD                =  14
    WRONG_USERNAME                =  15

    # user objects
    UNKNOWN_USER_ATTRIBUTE        =  16
    USER_NOT_FOUND                =  17
    USER_BLOCKED_SUCCESSFULLY     =  18
    USERNAME_ALREADY_EXISTS       =  19
    NO_USERS_FOUND                =  20
    USER_UNBLOCKED_SUCCESSFULLY   =  21
    NO_ADMINS_FOUND               =  22
    WRONG_VALUE                   =  23
    USER_DELETED_SUCCESSFULLY     =  24
    PROCESS_CANCELLED             =  25

    # admin 
    NO_LOGGED_IN_ADMIN            =  26
    ACCESS_DENIED                 =  27
    ADMIN_NOT_FOUND               =  28
    ADMIN_DELETED_SUCCESSFULLY    =  29
    NO_LOGGED_IN_USER             =  30
    LOGGED_ADMIN_OUT_SUCCESSFUL   =  31
    LOGGED_USER_OUT_SUCCESSFUL    =  32
    ADMIN                         =  33
    USER                          =  34
    INVALID_INPUT                 =  35
    WRONG_TOKEN                   =  36
    ACTION_ABORTED                =  37
    USER_ALREADY_BLOCKED          =  38
    USER_ALREADY_UNBLOCKED        =  39
    