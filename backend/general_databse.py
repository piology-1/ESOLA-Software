import sqlite3
from datetime import datetime
import pandas as pd # for printing purposes, when debugging/ developing on the PC
# pandas still needs to be installed on Raspberry Pi for a successful running


class Database:
    """
    A class representing a SQLite database.

    This class can be used to create and manage a SQLite database.
    The different methods use SQL queries to edit the database.

    Attributes:
    -----------
        None
        
    Instance Variables:
    -------------------
    __database_path (str):
        The path to the location of the database file.
        
    __database_name (str):
        The name of the database file.
    """


    def __init__(self, database_path: str, database_name: str) -> None:
        """
        Initializes an instance of the Database class.

        Args:
            database_path (str): The path to the location of the database file.
            database_name (str): The name of the database file.

        Returns:
            None
        """

        self.__database_path: str = database_path
        self.__database_name: str = database_name

        # establish a connection to the database
        with sqlite3.connect(self.__database_path) as db_conn:
            db_cursor: sqlite3.Cursor = db_conn.cursor()
            # Create a database and open it. If the database already exists, it just opens the database again
            db_cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.__database_name}(date_of_insert DATE, card_uid TEXT)")

        # NOTE: With the usage of the context manager, we don't need to worry about closing the database after making changes!

    def clear_content(self) -> None:
        """
        Deletes all entries of the database object.

        Returns:
            None
        """

        with sqlite3.connect(self.__database_path) as db_conn:
            db_cursor = db_conn.cursor()
            db_cursor.execute(f"DELETE FROM {self.__database_name}")

    def user_exists(self, card_uid: str) -> bool:
        """
        Checks if a record with the given card UID exists
        in the database object.
    
        Args:
            card_uid (str): The UID of the smartcard.
    
        Returns:
            bool: True if a record with the given card UID exists,
                  False otherwise.
        """

        with sqlite3.connect(self.__database_path) as db_conn:
            db_cursor: sqlite3.Cursor = db_conn.cursor()

            row_count = db_cursor.execute(
                f"SELECT COUNT(*) FROM {self.__database_name} WHERE card_uid=:card_uid", {"card_uid": card_uid}).fetchone()[0]   
            return row_count > 0

    def add_new_user(self, card_uid: str) -> bool:
        """
        Adds a new record with the given card UID and current
        date to the the database object.

        Args:
            card_uid (str): The UID of the smartcard.
        
        Returns:
            bool: True if the record is successfully added to
                  the database, False otherwise.
                

        NOTE:
        This function just executes the sql statement for inserting 
        a given card UID into the database. Tests, if the admin_uid
        is valid or if the user already exists in the databse (etc.)
        sould be made in the function, which calls this method!
        """

        # Open a connection to the database
        with sqlite3.connect(self.__database_path) as db_conn:
            try:
                # Get a cursor object to execute SQL statements
                db_cursor: sqlite3.Cursor = db_conn.cursor()

                insert_query: str = f"INSERT INTO {self.__database_name}(date_of_insert, card_uid) VALUES (:date_of_insert, :card_uid)"
                # NOTE: There are multiple different versions to use parameterized queries (f.ex. tuples)
                insert_values: dict = {"date_of_insert": datetime.now().strftime("%d.%m.%Y; %H:%M"),
                                       "card_uid": card_uid}

                db_cursor.execute(insert_query, insert_values)

                return True
            except Exception:
                return False

    def delete_user(self, card_uid: str) -> bool:
        """
        Deletes the record with the given card UID from
        the database object.

        Args:
            card_uid (str): The UID of the smartcard.

        Returns:
            bool: True if the record is successfully deleted from
                  the database, False otherwise.
        
        NOTE:
        Just execute the SQL delete statement.
        No tests for validation etc. here!
        """

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

    def print_content(self) -> None:
        """
        Prints all data from the database object using
        the pandas library.

        Returns:
            None
        """

        with sqlite3.connect(self.__database_path) as db_conn:
            print(pd.read_sql_query(
                f"SELECT * FROM {self.__database_name}", db_conn).to_string(index=False))

    def export_to(self) -> None:
        """
        Exports the database data to another format, such as CSV or Excel (not yet implemented).
        Could be maybe useful in the future.
        For example maintaining databases.

        Returns:
            None
        """

        raise NotImplementedError
