from secrets import compare_digest
from functools import cached_property
import sqlite3

from system.data_user import User as du
from system.sql import SQLCommands as sqlc
from system.info_types import InfoTypes as it


class User:
    """ A real implementation of the user data class """
    def __init__(self):
        self.logged_in_user = None
        self.commands = sqlc.initialize_commands()

    
    @cached_property
    def __user_db(self):
        return r"User\userdata.db"


    @cached_property
    def __init_table(self):
        with sqlite3.connect(self.__user_db) as conn:
            _cursor = conn.cursor()
            try:
                _cursor.execute(self.commands.create_user_table)
            except sqlite3.OperationalError:
                return it.TABLE_ALREADY_EXISTS
            else:
                return it.TABLE_CREATED_SUCCESSFULLY

    
    @staticmethod
    def _parse_user(data):
        """
        Parses the user data from the database to format that
        can be used to construct a user object.

        :param data: data from the database
        :type data: as returned by cursor.fetchone()
        """
        data_dict = {key: value for key, value in zip(data.keys(), data)}
        return data_dict

    

    def create_account(self, data):
        """ Registers a new user into the database

        :param data: a tuple of the needed data to construct a user class
        :type data: tuple
        """
        with sqlite3.connect(self.__user_db) as conn:
            self.__init_table
            _cursor = conn.cursor()
            try:
                _cursor.execute(self.commands.insert_user_data, data)
            except sqlite3.IntegrityError:
                return it.USERNAME_ALREADY_EXISTS
            else:
                conn.commit()
                return it.CREATE_ACCOUNT_SUCCESSFUL

    
    def login_user(self, username, password):
        """ Tries to log a user in

        :param username: username of the user
        :type username: str
        :param password: password
        :type password: str
        """
        with sqlite3.connect(self.__user_db) as conn:
            conn.row_factory = sqlite3.Row
            _cursor = conn.cursor()
            try:
                _cursor.execute(self.commands.get_login_user, (username,))
            except sqlite3.OperationalError:
                return it.TABLE_NOT_FOUND
            else:
                if result := _cursor.fetchone():
                    user = du.from_dict(**self._parse_user(result))
                    if compare_digest(password, user.password):
                        self.logged_in_user = user
                        return it.LOGIN_SUCCESSFUL
                    return it.WRONG_PASSWORD
                return it.ACCOUNT_NOT_FOUND and it.WRONG_USERNAME
            


user = User()
data = (
    'teddbug',
    'Tedd',
    'Bug',
    17,
    'helloworld',
    ""
)
print(user.create_account(data))
print(user.login_user('teddbug', 'helloworld'))
print(bool(user.logged_in_user.blockstatus))