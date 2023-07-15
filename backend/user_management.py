# try:
from .general_databse import Database
from .Util import datadir
# except ImportError:
#     from general_databse import Database

#     def datadir() -> str:
#         import os
#         # is the path to the directory, where all the other directories such as backend, qml etc are located.
#         return str(os.getcwd())



class _UserManagement:
    """
    A class that manages both the admin and all users databases. It is based on the
    `Database` class in `general_database.py`, which represents a SQLite database.
    
    Attributes:
    -----------
    FRANKS_UID (str):
        The card UID of Mr. Frank.

    ARNOLDS_UID (str):
        The card UID of Mr. Arnold.
    
    ADMIN_DATABASE_NAME (str):
        The name of the database file for the admin database.
    
    ADMIN_DATABASE_PATH (str):
        The path to the database file for the admin database.
    
    ALL_USER_DATABASE_NAME (str):
        The name of the database file for the all users database.
    
    ALL_USER_DATABASE_PATH (str):
        The path to the database file for the all users database.

    Instance Variables:
    -------------------
    __admin_db (Database):
        An instance of the `Database` class representing the admin database.
    
    __all_users_db (Database):
        An instance of the `Database` class representing the all users database.
    """


    # default ADMIN UIDs
    FRANKS_UID: str = "04 91 23 72 79 5B 80"
    ARNOLDS_UID: str = "04 0D 35 72 79 5B 80"
    
    ADMIN_DATABASE_NAME: str = "admin_users"
    ADMIN_DATABASE_PATH: str = datadir() \
        + "/backend/databases/" + ADMIN_DATABASE_NAME + ".db"

    ALL_USER_DATABASE_NAME: str = "all_users"
    ALL_USER_DATABASE_PATH: str = datadir() \
        + "/backend/databases/" + ALL_USER_DATABASE_NAME + ".db"

    def __init__(self) -> None:
        """
        Initializes a new '_UserManagement' object. It creates the admin_db and all_users_db
        databases with the class variables and adds Mr. Frank's UID (ADMIN) to both of them,
        so the databases always have at least one user.
        It uses the `Database` class from `general_database.py`.
        
        Args:
            None

        Returns:
            None
        """

        self.__admin_db: Database = Database(database_path=self.ADMIN_DATABASE_PATH,
                                             database_name=self.ADMIN_DATABASE_NAME)
        

        self.__all_users_db: Database = Database(database_path=self.ALL_USER_DATABASE_PATH,
                                                 database_name=self.ALL_USER_DATABASE_NAME)
        
        # set the card UID of Mr. Frank to both databases, so they are never empty, after initialization
        if not self.__admin_db.user_exists(card_uid=self.FRANKS_UID):
            # user does not exist yet
            self.__admin_db.add_new_user(card_uid=self.FRANKS_UID)
        
        if not self.__all_users_db.user_exists(card_uid=self.FRANKS_UID):
            self.__all_users_db.add_new_user(card_uid=self.FRANKS_UID)

        # set the card UID of Mr. Arnold to both databases, so they are never empty, after initialization
        if not self.__admin_db.user_exists(card_uid=self.ARNOLDS_UID):
            # user does not exist yet
            self.__admin_db.add_new_user(card_uid=self.ARNOLDS_UID)
        
        if not self.__all_users_db.user_exists(card_uid=self.ARNOLDS_UID):
            self.__all_users_db.add_new_user(card_uid=self.ARNOLDS_UID)

    @staticmethod
    def clear_db(database: Database) -> bool:
        """
        Clears the content of a given `Database` object by calling its `clear_content()` method.

        Args:
            database (Database): A `Database` object to be cleared.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        
        try:
            database.clear_content()
            return True
        except Exception:
            return False

    def clear_db_by_bool(self, all_users_db: bool = False, admin_db: bool = False) -> bool:
        """

        NOTE:
            This method is not used
        """
        
        # check if at least one database needs to be cleared
        if not (all_users_db or admin_db):
            return False

        # clear specified databases
        if all_users_db:
            self.__all_users_db.clear_content()
        if admin_db:
            self.__admin_db.clear_content()

        return True

    @staticmethod
    def force_add_user_by_uid(database: Database, uid: str) -> bool:
        """
        Adds a user to a given database.

        This method adds a user (card UID) to the given database without any
        tests or validations regarding permissions etc.
        It should be used carefully and with the knowledge of what you are doing.

        Args:
            database (Database): The database to add the user to.
            uid (str): The unique identifier of the user to be added.

        Returns:
            bool: True if the user was successfully added, False otherwise.
        """
        
        if database.user_exists(card_uid=uid):
            # user already exists in the given database
            return False

        return database.add_new_user(card_uid=uid)

    @staticmethod
    def force_delete_user(database: Database, uid: str) -> bool:
        """
        Deletes a user from a given database.

        This method deletes a user (card UID) from the given database without any
        tests or validations regarding permissions etc.
        It should be used carefully and with the knowledge of what you are doing.

        Args:
            database (Database): The database to delete user from.
            uid (str): The unique identifier of the user to be deleted.

        Returns:
            bool: True if the user was successfully deleted, False otherwise.
        """
        
        if not database.user_exists(card_uid=uid):
            # user does not exist in the DB and therefore cannot be deleted
            return False

        return database.delete_user(card_uid=uid)

    def add_user_by_uid(self, database: Database, user_uid: str, admin_uid: str) -> bool:
        """
        Adds a new user to a given database.

        This method adds a new user with the given UID to the specified database.
        The `admin_uid` parameter grants access to `database` and  must be valid for
        the adding to be successful.

        Args:
            database (Database): The database to which to add the user.
            user_uid (str): The unique identifier of the user to be added.
            admin_uid (str): The unique identifier of the admin that has permission to add a new user.

        Returns:
            bool: True if the user was successfully added, False otherwise.
        """
        
        if database.user_exists(card_uid=user_uid):
            # user already exists in the given database
            return False

        if not self.__admin_db.user_exists(card_uid=admin_uid):
            # The passed Admin UID is invalid and does not have permission to add a new user
            return False

        # At this point, the given UID does not already exists and the admin UID is valid
        if database.add_new_user(card_uid=user_uid):
            # new user has been added succesfully
            return True
        else:
            return False
        # == return database.add_new_user(card_uid=user_uid)

    def delete_user(self, database: Database, user_uid: str, admin_uid: str) -> bool:
        """
        Deletes a user with the given UID from the specified database.

        The `admin_uid` parameter must be valid for the deletion to be successful.

        Args:
            database (Database): The database from which to delete the user.
            user_uid (str): The unique identifier of the user to be deleted.
            admin_uid (str): The unique identifier of the admin that has permission to delete a user.

        Returns:
            bool: True if the user was successfully deleted, False otherwise.
        """

        if not database.user_exists(card_uid=user_uid):
            # user does not exist in the DB and therefore cannot be deleted
            return False

        if not self.__admin_db.user_exists(card_uid=admin_uid):
            # The passed Admin UID is invalid and does not have permission to delete an user
            return False

        # At this point, the given UID does exists and the admin UID is valid
        if database.delete_user(card_uid=user_uid):
            # new user has been removed succesfully
            return True
        else:
            return False
        # == return database.delete_user(card_uid=user_uid)


    def user_is_in_db(self, database: Database, user_uid: str) -> bool:
        """
        Checks if a user with the given UID exists in the given database.

        Args:
            database (Database): The database to check for the user's existence.
            user_uid (str): The unique identifier of the user to check.

        Returns:
            bool: True if the user exists in the database, False otherwise.
        """
        return database.user_exists(card_uid=user_uid)

    ### debug methods ###
    @staticmethod
    def print_db(database: Database) -> None:
        """
        Prints the content of the specified database to the console.

        Args:
            database (Database): The database to print to the console.
        Returns:
            None
        """

        database.print_content()
        print()

    @property
    def all_users_db(self) -> Database:
        """
        Getter for the private attribute __all_users_db.

        Returns:
            Database: The database containing information about all users.
        """
        
        return self.__all_users_db

    @property
    def admin_db(self) -> Database:
        """
        Getter for the private attribute __admin_db.

        Returns:
            Database: The database containing information about admin users.
        """
        
        return self.__admin_db


UserManagement: _UserManagement = _UserManagement()

## --> uncomment to import lines above to execute this file directly without starting the
## whole GUI and access the UserManagement object
## possible commands are:
# UserManagement.print_db(database=UserManagement.all_users_db)
# UserManagement.print_db(database=UserManagement.admin_db)

# NOTE: relative imports (.general_databse, or .Util) are needed for the Raspberry Pi to work properly
# So make sure that the file in the backend directory all uses relative imports, if the code runs on the Raspberry Pi