from enum import Enum, unique

@unique
class Permission(Enum):
    """ Admin permissions or privileges """

    # DANGER ZONE
    DELETE_USER      = 1
    DELETE_ADMIN     = 2
    CLEAR_DATABASE   = 3
    SEE_ALL_USERS    = 4
    
    # SERIOUS ZONE
    BLOCK_USER       = 6
    UNBLOCK_USER     = 7

    # NORMAL ZONE
    SEARCH_USER      = 8
    SEARCH_ADMIN     = 9
    GET_USERS_COUNT  = 10
    SEE_ALL_ADMINS   = 5
    GET_ADMINS_COUNT = 11
    
