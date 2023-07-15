import sqlite3
from datetime import datetime
import pandas as pd


class Database:

    def __init__(self, database_path: str, database_name: str):

        self.__database_path: str = database_path
        self.__database_name: str = database_name

        # establish a connection to the admin users database
        with sqlite3.connect(self.__database_path) as db_conn:
            db_cursor: sqlite3.Cursor = db_conn.cursor()
            # Create a database and open it. If the database already exists, it just opens the database again
            db_cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.__database_name}(date_of_insert DATE, card_uid TEXT)")

            # If there is no card_uid in the database, add one for test purposes
            # db_cursor.execute("SELECT COUNT(*) FROM admin_users")
            # if db_cursor.fetchone()[0] == 0:
            #     db_cursor.execute("INSERT INTO admin_users(date_of_insert, card_uid) VALUES (:date_of_insert, :card_uid)", {
            #         "date_of_insert": datetime.now(),
            #         "card_uid": "04 2B 7B 2A 54 61 80"})

        # NOTE: With the usage of the context manager, we don't need to worry about closing the database after making changes!

    def clear_content(self) -> None:
        with sqlite3.connect(self.__database_path) as db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.execute(f"DELETE FROM {self.__database_name}")

    def user_exists(self, card_uid: str) -> bool:
        with sqlite3.connect(self.__database_path) as db_conn:
            db_cursor: sqlite3.Cursor = db_conn.cursor()

            row_count = db_cursor.execute(
                f"SELECT COUNT(*) FROM {self.__database_name} WHERE card_uid=:card_uid", {"card_uid": card_uid}).fetchone()[0]
            return row_count > 0

            # check if the given uid is present in the all users database
            # db_cursor.execute(
            #     f"SELECT * FROM {self.__database_name} WHERE card_uid=:card_uid", {"card_uid": card_uid})
            # return db_cursor.fetchone() is not None

    def add_new_user(self, card_uid: str) -> bool:
        # NOTE: This function just executes the sql statement for inserting a new user into the database.
        # Tests, if the admin_uid is valid or if the user already exists in the databse sould be made in the function, which calls this method!

        # Open a connection to the database
        with sqlite3.connect(self.__database_path) as db_conn:
            try:
                # Get a cursor object to execute SQL statements
                db_cursor: sqlite3.Cursor = db_conn.cursor()

                insert_query: str = f"INSERT INTO {self.__database_name}(date_of_insert, card_uid) VALUES (:date_of_insert, :card_uid)"
                # NOTE: There are multiple different versions to use parameterized queries (f.ex. tuples)
                insert_values: dict = {"date_of_insert": datetime.now(),
                                       "card_uid": card_uid}

                db_cursor.execute(insert_query, insert_values)

                return True
            except Exception:
                return False

    def delete_user(self, card_uid: str) -> bool:
        # NOTE: Just execute the SQL delete statement. No tests for validation here!

        # Open a connection to the database
        with sqlite3.connect(self.__database_path) as db_conn:
            try:
                # Get a cursor object to execute SQL statements
                db_cursor: sqlite3.Cursor = db_conn.cursor()

                delete_query: str = f"DELETE FROM {self.__database_name} WHERE card_uid=:card_uid"
                # NOTE: There are multiple different versions to use parameterized queries (f.ex. tuples)
                delete_values: dict = {"card_uid": card_uid}
                db_cursor.execute(delete_query, delete_values)

                return True
            except Exception:
                return False

    def print_content(self):
        with sqlite3.connect(self.__database_path) as db_conn:
            print(pd.read_sql_query(
                f"SELECT * FROM {self.__database_name}", db_conn).to_string(index=False))

    def export_to(self):
        pass


# def datadir() -> str:
#     import os
#     # is the path to the directory, where all the other directories such as backend, qml etc are located.
#     return str(os.getcwd())


# admin_db = Database(database_path=datadir() + "/unittests/user_management_DB/databases/admin_users.db",
#                     database_name="admin_users")
# admin_db.print_content()

# all_users_db = Database(database_path=datadir() + "/unittests/user_management_DB/databases/all_users.db",
#                         database_name="all_users")
# all_users_db.print_content()

# admin_db.add_new_user(card_uid="04 2B 7B 2A 54 61 80")
# admin_db.print_content()

# admin_db.clear_content()
# admin_db.print_content()
