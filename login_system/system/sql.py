from dataclasses import dataclass


@dataclass
class SQLCommands:
    """ A dataclass to host sql commands """
    block_user: str
    unblock_user: str
    get_all_users: str
    get_all_admins: str
    clear_database: str
    get_login_user: str
    get_users_count: str
    get_login_admin: str
    delete_user_data: str
    get_admins_count: str
    insert_user_data: str
    create_user_table: str
    delete_admin_data: str
    insert_admin_data: str
    create_admin_table: str
    

    @classmethod
    def initialize_commands(cls):
        """ Initializes the commands """

        commands = {
            "create_admin_table": """

                CREATE TABLE admin (
                        username VARCHAR(30) NOT NULL UNIQUE PRIMARY KEY,
                        firstname VARCHAR(30) NOT NULL,
                        lastname VARCHAR(30) NOT NULL,
                        age INTEGER NOT NULL,
                        CHECK (age >= 8)
                        password VARCHAR(50) NOT NULL,
                        type INTEGER NOT NULL
                        CHECK (type in (1, 2, 3))
                        );
            """,

            # user table
            "create_user_table": """

                CREATE TABLE users (
                        username VARCHAR(25) NOT NULL UNIQUE PRIMARY KEY,
                        firstname VARCHAR(25) NOT NULL,
                        lastname VARCHAR(25) NOT NULL,
                        age INTEGER NOT NULL CHECK (age >= 8),
                        password VARCHAR(20) NOT NULL,
                        blockstatus BOOLEAN DEFAULT false
                        );
            """, 

            # insert into admin 
            "insert_admin_data": """
            INSERT INTO admin
                VALUES
                    (?, ?, ?, ?, ?, ?);
            """,

            # insert into user
            "insert_user_data": """

                INSERT INTO users
                    VALUES
                        (?, ?, ?, ?, ?, ?);
            """,

            # get admin login
            "get_login_admin": """

                SELECT * FROM admin WHERE username = ? ;
            """,

            # get user login
            "get_login_user": """

                SELECT * FROM users WHERE username = ? ;
            """,

            "get_all_users": """
            
                SELECT * FROM users;
            """,

            "get_all_admins": """
            
                SELECT * FROM admin;
            """,

            "get_admins_count": """
            
                SELECT COUNT() as "Number of admins" from admin;
            """,

            "get_users_count": """
            
                SELECT COUNT() as "Number of users" from users;
            """,

            # delete an admin account
            "delete_admin_data": """

                DELETE FROM admin WHERE username = ? ;
            """,

            # delete user account
            "delete_user_data": """

                DELETE FROM users WHERE username = ? ;
            """,

            "block_user": """

                UPDATE users
                  SET blockstatus = true WHERE username = ? ; 
            """,

            "unblock_user": """

                UPDATE users
                  SET blockstatus = false WHERE username = ? ; 
            """,

            "clear_database": """
            
                DROP TABLE users;
                
            """
        }

        return cls(**commands)
