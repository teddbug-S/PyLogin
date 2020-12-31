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
    LOGIN_SUCCESSFUL              =  12
    WRONG_PASSWORD                =  13
    WRONG_USERNAME                =  14

    # user objects
    UNKNOWN_USER_ATTRIBUTE        =  15
    USER_NOT_FOUND                =  16
    USER_BLOCKED_SUCCESSFULLY     =  17
    USERNAME_ALREADY_EXISTS       =  18
    NO_USERS_FOUND                =  19
    USER_UNBLOCKED_SUCCESSFULLY   =  20
    NO_ADMINS_FOUND               =  28
    WRONG_VALUE                   =  21
    USER_DELETED_SUCCESSFULLY     =  22
    PROCESS_CANCELLED             =  23

    # admin 
    NO_LOGGED_IN_ADMIN            =  24
    ACCESS_DENIED                 =  25
    ADMIN_NOT_FOUND               =  26
    ADMIN_DELETED_SUCCESSFULLY    =  27
    