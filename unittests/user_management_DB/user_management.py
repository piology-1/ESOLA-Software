from general_databse import Database


def datadir() -> str:
    import os
    # is the path to the directory, where all the other directories such as backend, qml etc are located.
    return str(os.getcwd())


class UserManagement:

    ADMIN_DATABASE_NAME: str = "admin_users"
    ADMIN_DATABASE_PATH: str = datadir() \
        + "/unittests/user_management_DB/databases/" + ADMIN_DATABASE_NAME + ".db"

    ALL_USER_DATABASE_NAME: str = "all_users"
    ALL_USER_DATABASE_PATH: str = datadir() \
        + "/unittests/user_management_DB/databases/" + ALL_USER_DATABASE_NAME + ".db"

    def __init__(self) -> None:
        self.__admin_db: Database = Database(database_path=self.ADMIN_DATABASE_PATH,
                                             database_name=self.ADMIN_DATABASE_NAME)

        self.__all_users_db: Database = Database(database_path=self.ALL_USER_DATABASE_PATH,
                                                 database_name=self.ALL_USER_DATABASE_NAME)

    @staticmethod
    def clear_db(database: Database) -> bool:
        try:
            database.clear_content()
            return True
        except Exception:
            return False

    def clear_db_by_bool(self, all_users_db: bool = False, admin_db: bool = False) -> bool:
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
            Adds a user to the given database without any tests and validations, regarding permissions etc.
            Should be used carefully and with the knowlege, what you are doing!!!
        """

        if database.user_exists(card_uid=uid):
            # user already exists in the given database
            return False

        return database.add_new_user(card_uid=uid)

    @staticmethod
    def force_delete_user(database: Database, uid: str) -> bool:
        """
            Deletes a user to the given database without any tests and validations, regarding permissions etc.
            Should be used carefully and with the knowlege, what you are doing!!!
        """

        if not database.user_exists(card_uid=uid):
            # user does not exist in the DB and therefore cannot be deleted
            return False

        return database.delete_user(card_uid=uid)

    def add_user_by_uid(self, database: Database, user_uid: str, admin_uid: str) -> bool:
        """
            database: the database, where the new user with the UID should be added
            user_uid: the user UID to be added to the database
            admin_uid: the admin UID to grant access to the database, where changes should be done.

            So, there can be make changes to both database (admin_db and all_user_db) within one method.
            admin_uid grants acces to all_user_db such as to admin_db
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

    ### debug methods ###
    @staticmethod
    def print_db(database: Database) -> None:
        database.print_content()
        print()

    @property
    def all_users_db(self) -> Database:
        return self.__all_users_db

    @property
    def admin_db(self) -> Database:
        return self.__admin_db

