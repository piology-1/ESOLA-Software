from PySide2.QtCore import QObject, Slot
from .Compartments import Compartments
from .rfid_reader import RFIDReader
from .user_management import UserManagement
from .rfid_reader_monitor import RFIDReaderManagement


class _BackendBridge(QObject):
    """
    A bridge between the backend and frontend of the application.

    This class provides methods to interact with the compartments of the battery management system. 
    It also manages communication between RFID readers and smartcards.
    In addition, it provides an interface to the UserManagement and the databases.

    Some methods are called using Signals and Slots to connect the backend with the frontend.
    This class is mainly utilized by the App.qml file.
    
    Attributes:
    -----------
        None
    
    Instance Variables:
    -------------------
        None
    """

    ### Methods for monitoring the RFID Reader ###
    @staticmethod
    def start_rfid_reader_monitoring() -> None:
        """
        Starts monitoring the RFID reader.
        Gets called in gui_main.py before starting the whole application.
        """

        RFIDReaderManagement.start()
    
    @staticmethod
    def end_rfid_reader_monitoring() -> None:
        """
        Stops monitoring the RFID reader.
        Gets called in gui_main.py after the application is finished.
        """

        RFIDReaderManagement.end()

    @Slot(str, result=list)
    def getAvailableComps(self, batteryType: str) -> list:
        """
        Returns a list of available compartments for the given battery type.
        """
        
        return Compartments.get_available(batteryType)

    @Slot(str, result=list)
    def getOccupiedComps(self, batteryType: str) -> list:
        """
        Returns a list of occupied compartments for the given battery type.
        """
        
        return Compartments.get_occupied(batteryType)

    ########## locking methods via RFID Reader and smartcards ##########
    @Slot(str, int, str, result=bool)
    def rfidLock(self, batteryType: str, index: int, card_uid: str) -> bool:
        """
        Locks a specific compartment for a given battery via the RFID Reader.
        """

        return Compartments.rfid_lock(batteryType, index, card_uid)

    @Slot(str, int, str, result=bool)
    def rfidUnlock(self, batteryType: str, index: int, card_uid: str) -> bool:
        """
        Unlocks a specifically locked compartment for a given battery via the RFID Reader.
        """

        return Compartments.rfid_unlock(batteryType, index, card_uid)

    @Slot(result=bool)
    def reader_is_available(self) -> bool:
        """
        Checks if the RFID reader is available or not.
        """

        return RFIDReader.is_available

    ########## read smartcard method #########
    @Slot(result=str)
    def scan_card(self) -> None:
        """
        Scans the smart card via the RFID reader.
        It sets the attributes of the instance 'RFIDReader',
        so they can be accessed from other getter methods.
        """
        RFIDReader.scan_card()

    @Slot(result=bool)
    def get_reading_status(self) -> bool:
        """
        Returns the status of the reading process, whether it was successful or not.
        """

        return RFIDReader.get_read_status

    @Slot(result=str)
    def get_card_uid(self) -> str:
        """
        Returns the UID of the last scanned card.
        """

        return RFIDReader.get_card_uid

    @Slot(result=str)
    def get_error_message(self) -> str:
        """
        Returns the error message received during the last RFID operation, if
        the scan wasn't successful.
        """

        return RFIDReader.get_error_message


    ########## USER MANAGEMENT #########
    # USER
    @Slot(str, result=bool)
    def user_exists_in_all_users_db(self, scanned_uid:str) -> bool:
        """
        Checks if the given user exists in the All Users database.
        """
        
        return UserManagement.user_is_in_db(database=UserManagement.all_users_db,
                                                    user_uid=str(scanned_uid))

    @Slot(str, str, result=bool)
    def add_new_user_to_all_users_db(self, new_user_uid: str, admin_uid: str) -> bool:
        """
        Adds a new user to the All Users database with an existing admin UID.
        """

        return UserManagement.add_user_by_uid(database=UserManagement.all_users_db,
                                              user_uid=new_user_uid,
                                              admin_uid=admin_uid)
    
    @Slot(str, str, result=bool)
    def delete_user_from_all_users_db(self, user_uid_to_delete: str, admin_uid: str) -> bool:
        """
        Deletes a user from the All Users database with an existing admin UID.
        """

        return UserManagement.delete_user(database=UserManagement.all_users_db,
                                              user_uid=user_uid_to_delete,
                                              admin_uid=admin_uid)
    
    # ADMIN
    @Slot(str, result=bool)
    def admin_exists_in_admin_db(self, scanned_uid:str) -> bool:
        """
        Checks if the given UID exists in the Admin database.
        """
        
        # also checks ,if the given card uid is a valid admin UID       
        return UserManagement.user_is_in_db(database=UserManagement.admin_db,
                                                    user_uid=str(scanned_uid))
    
    @Slot(str, str, result=bool)
    def add_new_admin_uid(self, new_admin_uid: str, exsiting_admin_uid: str) -> bool:
        """
        Adds a new admin to the Admin database with an existing admin UID.
        If an admin gets added, it also adds the corresponding card uid
        to the all users database.
        """

        adding_ret_val: bool = UserManagement.add_user_by_uid(database=UserManagement.all_users_db,
                                              user_uid=new_admin_uid,
                                              admin_uid=exsiting_admin_uid) \
                            and UserManagement.add_user_by_uid(database=UserManagement.admin_db,
                                              user_uid=new_admin_uid,
                                              admin_uid=exsiting_admin_uid)
        
        return adding_ret_val
    
    @Slot(str, str, result=bool)
    def delete_admin_uid(self, admin_uid_to_delete: str, exsiting_admin_uid: str) -> bool:
        """
        Deletes an admin from the Admin database with an existing admin UID.
        If an admin gets deleted, it also removes the corresponding card uid
        from the all users database.
        """

        del_ret_val: bool = UserManagement.delete_user(database=UserManagement.all_users_db,
                                              user_uid=admin_uid_to_delete,
                                              admin_uid=exsiting_admin_uid) \
                            and UserManagement.delete_user(database=UserManagement.admin_db,
                                                           user_uid=admin_uid_to_delete,
                                                           admin_uid=exsiting_admin_uid)
        
        return del_ret_val
    

BackendBridge: _BackendBridge = _BackendBridge()  # this instance gets called in gui_main.py
