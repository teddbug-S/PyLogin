import sqlite3
from secrets import compare_digest
from pprint import pprint
from functools import cached_property

from system.data_admin import Admin as da
from system.data_user import User as du
from system.info_types import InfoTypes as it
from system.data_admin import AdminType as at
from system.sql import SQLCommands as sqlc
from system.permissions import Permission as p



class Admin:
    """ A real implementation of the Admin """

    def __init__(self) -> None:
        self.logged_in_admin = None
        self.commands = sqlc.initialize_commands()
        self.admin_types = at

    @cached_property
    def __user_db(self):
        return r"User\userdata.db"

    @cached_property
    def __admin_db(self):
        return r"Admin\admindata.db"

    @cached_property
    def __init_table(self):
        _connection = sqlite3.connect(self.__admin_db)
        _cursor = _connection.cursor()
        try:
            _cursor.execute(self.commands.create_admin_table)
        except sqlite3.OperationalError:
            return it.TABLE_ALREADY_EXISTS
        else:
            return it.TABLE_CREATED_SUCCESSFULLY

    
    @staticmethod
    def _parse_admin(data):
        """ Parses data from sqlite fetchone to an Admin object

        :param data: data to parse
        :type data: tuple
        :return: Admin object
        :rtype: Admin
        """
        data_dict = {}
        for key, value in zip(data.keys(), data):
            if key == 'type':
                for type in at:
                    value = type if type.value == value else value
            data_dict[key] = value

        return data_dict

    
    @staticmethod
    def _parse_user(data):
        """
        Parses the user data from the database to a format that
        can be used to construct a user object.

        :param data: data from the database
        :type data: as returned by cursor.fetchone() according to the row_factory
        """
        data_dict = {}
        for key, value in zip(data.keys(), data):
            if key in ('blockstatus', 'verified'):
                value = bool(value)
            data_dict[key] = value
        return data_dict

    
    def _get_usernames(self):
        """
        Returns all usernames from the user database
        """
        with sqlite3.connect(self.__user_db) as conn:
            _cursor = conn.cursor()
            try:
                _cursor.execute(self.commands.get_all_user_usernames) # execute get all user userames sql
                data = tuple(name for i in _cursor.fetchall() for name in i) # fetch data
            except sqlite3.OperationalError:
                return it.TABLE_NOT_FOUND
        return data
    
    def _get_admin_usernames(self):
        """
        Returns all usernames from the admin database
        """
        with sqlite3.connect(self.__admin_db) as conn:
            _cursor = conn.cursor()
            try:
                _cursor.execute(self.commands.get_all_admin_usernames) # execute get all user userames sql
                data = tuple(name for i in _cursor.fetchall() for name in i) # fetch data
            except sqlite3.OperationalError:
                return it.TABLE_NOT_FOUND
        return data


    def create_account(self, data):
        """ Creates an Admin account

        Note that all the data received must be processed
        before passing into the create_account method.
        """
        with sqlite3.connect(self.__admin_db) as conn:
            conn.row_factory = sqlite3.Row
            _cursor = conn.cursor()
            self.__init_table
            try:
                _cursor.execute(self.commands.insert_admin_data, data)
            except sqlite3.IntegrityError:
                return it.USERNAME_ALREADY_EXISTS
            else:
                conn.commit()
                return it.CREATE_ACCOUNT_SUCCESSFUL


    def login_admin(self, username, password):
        """ Tries to log username and password in as an admin. """
        # opens the db
        with sqlite3.connect(self.__admin_db) as conn:
            conn.row_factory = sqlite3.Row
            _cursor = conn.cursor() # get cursor
            try:
                # get creds
                _cursor.execute(self.commands.get_login_admin, (username,))
            except sqlite3.OperationalError:
                # if table not initialized
                return it.TABLE_NOT_FOUND
            else:
                # else let's authenticate
                _data = _cursor.fetchone()
                if _data:
                    _admin = da.from_dict(**self._parse_admin(_data))
                    if compare_digest(username, _admin.username):
                        if compare_digest(password, _admin.password):
                            self.logged_in_admin = _admin
                            return it.LOGIN_ADMIN_SUCCESSFUL
                        else:
                            return it.WRONG_PASSWORD
                else:
                    return it.WRONG_USERNAME or it.USER_NOT_FOUND

    
    def _delete_user(self, username):
        """ Provides an interface for deleting a user from the database

        :param username: username to be deleted
        :type username: str

        Note that only an admin of type AdminType.ALMIGHTY has access to this method.
        """
        try:
            if self.logged_in_admin.type in (at.ALMIGHTY, at.STANDARD,):
                with sqlite3.connect(self.__user_db) as conn:
                    _cursor = conn.cursor()
                    try:
                        _cursor.execute(self.commands.delete_user_data, (username,))
                    except sqlite3.OperationalError:
                        return it.TABLE_NOT_FOUND
                    else:
                        conn.commit()
                        if not _cursor.rowcount:
                            return it.USER_NOT_FOUND
                        return it.USER_DELETED_SUCCESSFULLY
            else:
                return it.ACCESS_DENIED
        except AttributeError:
            return it.NO_LOGGED_IN_ADMIN

    
    def _delete_admin(self, username):
        """
        Provides an interface to delete an admin

        :param username: username of admin to be deleted
        :type username: str

        Note that only an admin of type AdminType.ALMIGHTY has access to this method.
        """
        try:
            if self.logged_in_admin.type == at.ALMIGHTY:
                with sqlite3.connect(self.__admin_db) as conn:
                    _cursor = conn.cursor()
                    try:
                        _cursor.execute(self.commands.delete_admin_data, (username,))
                    except sqlite3.OperationalError:
                        return it.TABLE_NOT_FOUND
                    else:
                        conn.commit()
                        if not _cursor.rowcount:
                            return it.ADMIN_NOT_FOUND
                        return it.ADMIN_DELETED_SUCCESSFULLY
            else:
                return it.ACCESS_DENIED
        except AttributeError:
            return it.NO_LOGGED_IN_ADMIN

    
    def _clear_database(self):
        """
        Clears the entire database

        Note that this method is only available to the admin of type AdminType.ALMIGHTY
        """
        try:
            if self.logged_in_admin.type == at.ALMIGHTY:
                with sqlite3.connect(self.__user_db) as conn:
                    _cursor = conn.cursor()
                    try:
                        _cursor.execute(self.commands.clear_database)
                    except sqlite3.OperationalError:
                        return it.TABLE_NOT_FOUND
                    else:
                        return it.DATABASE_CLEARED_SUCCESSFULLY
            else:
                return it.ACCESS_DENIED
        except AttributeError:
            return it.NO_LOGGED_IN_ADMIN




    def show_permissions(self):
        """ Returns the privileges of the currently logged in admin. """
        try:
            if self.logged_in_admin.type == at.ALMIGHTY:
                _permissions = tuple(perm for perm in p)
            elif self.logged_in_admin.type == at.STANDARD:
                _permissions = tuple(perm for perm in p if perm not in (p.DELETE_ADMIN, p.CLEAR_DATABASE,))
            else:
                _permissions = (
                    p.BLOCK_USER,
                    p.UNBLOCK_USER,
                    p.SEARCH_USER,
                    p.GET_USERS_COUNT,
                    p.SEE_ALL_ADMINS,
                    p.GET_ADMINS_COUNT,
                   
                )
            
            return _permissions
        except AttributeError:
            return it.NO_LOGGED_IN_ADMIN


    def search_admin(self, username):
        """ Provides an interface for searching an admin of any type.

        :param username: admin's username
        :type username: str

        Note that an admin of type AdminType.GUEST is not allowed to access this method.
        """
        try:
            if self.logged_in_admin.type in (type for type in at):
                with sqlite3.connect(self.__admin_db) as conn:
                    conn.row_factory = sqlite3.Row
                    _cursor = conn.cursor()
                    try:
                        _cursor.execute(self.commands.get_login_admin, (username,))
                    except sqlite3.OperationalError:
                        return it.TABLE_NOT_FOUND
                    else:
                        if result := _cursor.fetchone():
                            return da.from_dict(**self._parse_admin(result))
                        else:
                            return it.ADMIN_NOT_FOUND
            else:
                return it.ACCESS_DENIED
        except AttributeError:
            return it.NO_LOGGED_IN_ADMIN


    def search_user(self, username):
        """ Provides an interface for searching a
            specific user from the data base """
        try:
            if self.logged_in_admin.type in (type for type in at):
                with sqlite3.connect(self.__user_db) as conn:
                    conn.row_factory = sqlite3.Row
                    _cursor = conn.cursor()
                    try:
                        _cursor.execute(self.commands.get_login_user,(username,) )
                    except sqlite3.OperationalError:
                        return it.TABLE_NOT_FOUND
                    else:
                        if result := _cursor.fetchone():
                            user = du.from_dict(**self._parse_user(result))
                            return user
                        else:
                            return it.USER_NOT_FOUND
            else:
                return it.ACCESS_DENIED
        except AttributeError:
            return it.NO_LOGGED_IN_ADMIN

    
    def get_all_users(self):
        """ Returns every data all users from the database """
        try:
            if self.logged_in_admin.type in (at.ALMIGHTY, at.STANDARD):
                with sqlite3.connect(self.__user_db) as conn:
                    conn.row_factory = sqlite3.Row
                    _cursor = conn.cursor()
                    try:
                        _cursor.execute(self.commands.get_all_users)
                    except sqlite3.OperationalError:
                        return it.TABLE_NOT_FOUND
                    else:
                        result = _cursor.fetchall()
                        if result:
                            users = tuple(du.from_dict(**self._parse_user(user)) for user in result)
                            return users
                        else:
                            return it.NO_USERS_FOUND
            else:
                return it.ACCESS_DENIED
        except AttributeError:
            return it.NO_LOGGED_IN_ADMIN

    
    def get_all_admins(self):
        """ Returns every data on all the users from the database """
        try:
            if self.logged_in_admin.type in (at.ALMIGHTY, at.STANDARD, at.GUEST):
                with sqlite3.connect(self.__admin_db) as conn:
                    conn.row_factory = sqlite3.Row
                    _cursor = conn.cursor()
                    try:
                        _cursor.execute(self.commands.get_all_admins, (self.logged_in_admin.username,))
                    except sqlite3.OperationalError:
                        return it.TABLE_NOT_FOUND
                    else:
                        if result := _cursor.fetchall():
                            admins = tuple(da.from_dict(**self._parse_admin(admin)) for admin in result)
                            return admins
                        else:
                            return it.NO_ADMINS_FOUND
            else:
                return it.ACCESS_DENIED
        except AttributeError:
            return it.NO_LOGGED_IN_ADMIN
            



    def block_user(self, username):
        """ Blocks a user

        :param username: username of user to be blocked
        :type username: str
        """
        try:
            if self.logged_in_admin.type in (type for type in at):
                with sqlite3.connect(self.__user_db) as conn:
                    _cursor = conn.cursor()
                    try:
                        _cursor.execute(self.commands.block_user, (username,))
                    except sqlite3.IntegrityError:
                        return it.WRONG_VALUE
                    except sqlite3.OperationalError:
                        return it.TABLE_NOT_FOUND
                    else:
                        if not _cursor.rowcount:
                            return it.USER_NOT_FOUND
                        else:
                            conn.commit()
                            return it.USER_BLOCKED_SUCCESSFULLY
            else:
                return it.ACCESS_DENIED
        except AttributeError:
            return it.NO_LOGGED_IN_ADMIN


    def unblock_user(self, username):
        """ Unblocks a user

        :param username: username of user to be unblocked
        :type username: str
        """
        try:
            if self.logged_in_admin.type in (type for type in at):
                with sqlite3.connect(self.__user_db) as conn:
                    _cursor = conn.cursor()
                    try:
                        _cursor.execute(self.commands.unblock_user, (username,))
                    except sqlite3.IntegrityError:
                        return it.WRONG_VALUE
                    else:
                        if not _cursor.rowcount:
                            return it.USER_NOT_FOUND
                        else:
                            conn.commit()
                            return it.USER_UNBLOCKED_SUCCESSFULLY
            else:
                return it.ACCESS_DENIED
        except AttributeError:
            return it.NO_LOGGED_IN_ADMIN

    
    def get_users_count(self):
        """ Returns the number of all users in the database """
        try:
            if self.logged_in_admin.type in (type for type in at):
                with sqlite3.connect(self.__user_db) as conn:
                    _cursor = conn.cursor()
                    try:
                        _cursor.execute(self.commands.get_users_count)
                    except sqlite3.OperationalError:
                        return it.TABLE_NOT_FOUND
                    else:
                        return _cursor.fetchone()[0]
            else:
                return it.ACCESS_DENIED
        except AttributeError:
            return it.NO_LOGGED_IN_ADMIN

    
    def get_admins_count(self):
        """ Returns the number of all admins in the database """
        try:
            if self.logged_in_admin.type in (type for type in at):
                with sqlite3.connect(self.__admin_db) as conn:
                    _cursor = conn.cursor()
                    try:
                        _cursor.execute(self.commands.get_admins_count)
                    except sqlite3.OperationalError:
                        return it.TABLE_NOT_FOUND
                    else:
                        return _cursor.fetchone()[0]
            else:
                return it.ACCESS_DENIED
        except AttributeError:
            return it.NO_LOGGED_IN_ADMIN
