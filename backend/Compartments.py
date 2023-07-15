import json
from .Locks import Locks
from .rfidLock import RFIDLock
from .Hardware import Hardware
from . import Util


class _Compartments:
    """
    This class provides and manages all data related to the compartments.
    
    Attributes:
    -----------
        None
    
    Instance Variables:
    -------------------
    _by_battery_type (dict):
        Dictionary that maps each battery type to a list of available
        compartments.
    """

    class _Compartment:
        """
        This inner class holds data specific to one Compartment.

        Attributes:
        -----------
        None
            
        Instance Variables:
        -------------------
        door (int):
            Door number of the compartment

        pos (int):
            Position of the tower
        """


        def __init__(self, door_numb: int, tower_pos: int) -> None:
            """
            Initializes a new '_Compartment' object.

            Args:
                door_numb (int): Door number of the compartment.
                tower_pos (int): Position of the tower.

            Returns:
                None
            """

            self.door: int = int(door_numb)
            self.pos: int = int(tower_pos)

    def __init__(self) -> None:
        """
            Initializes a new `_Compartments` object.

            This object represents the compartments used to store batteries.
            It retrieves data from the 'compartments.json' file located in the main directory
            and creates a dictionary that maps each battery type to a list of available compartments.
            Therefore it converts each 2D-List for each battery type into a 1D List.
            Each element in the list is either a `_Compartment` object (if the compartment exists)
            or None (if it does not exist).

            Example of self._by_battery_type:

            {
            'bosch': [
                <backend.Compartments._Compartment object at 0x000002506D14ECB0>,
                None,
                None,
                None,
                <backend.Compartments._Compartment object at 0x000002506D14EC20>,
                None,
                None,
                None
            ],
            'panasonic': [
                <backend.Compartments._Compartment object at 0x000002506C334D90>,
                None,
                None, 
                None,
                <backend.Compartments._Compartment object at 0x000002506D14EB60>,
                None,
                None,
                None
            ],
            'panterra': [
                <backend.Compartments._Compartment object at 0x000002506D14EBC0>,
                None,
                None,
                None
            ]
        }

        Returns:
            None.
        """

        # create an empty dictionary for each battery type
        self._by_battery_type: dict = {}

        # Open the compartments JSON-file saved in the main curretn working directory
        with open(Util.datadir() + "/compartments.json") as f:
            for battery_type, buttons in json.load(f).items():
                if battery_type == "_comment":  # ignore the comments in the JSON file
                    continue

                # flatten the 2D-List into a 1D-List
                __new_button_list: list = []
                for door_and_pos in buttons:
                    if door_and_pos and len(door_and_pos) == 2:
                        __new_button_list.append(
                            self._Compartment(
                                door_numb=door_and_pos[0], tower_pos=door_and_pos[1]
                            )
                        )
                    else:
                        __new_button_list.append(None)

                self._by_battery_type[battery_type] = __new_button_list

    def get_available(self, battery_type: str) -> list[bool]:
        """
        Returns a list indicating whether each compartment for a given battery type is available.

        The returned list has the same length as the number of compartments for the given
        battery type. Each element in the list corresponds to a compartment and can be:

        - True if the compartment is available (i.e., unoccupied)
        - False if the compartment is occupied
        - None if the compartment does not exist (i.e., is None)

        Args:
            battery_type (str): The type of battery whose compartments to check.

        Returns:
            A list of bool or None indicating the availability status of each compartment.
        """

        __compartments = self._by_battery_type[battery_type]
        __ret_list = []
        for compartment in __compartments:
            if compartment:
                __ret_list.append(
                    not Locks.is_present(compartment.door, compartment.pos)
                )  # returns True or False
            else:  # element/ compartment is None
                __ret_list.append(None)

        return __ret_list

    def get_occupied(self, battery_type: str) -> list[bool]:
        """
        Returns a list indicating whether each compartment for a given battery type is occupied.

        The returned list has the same length as the number of compartments for the given
        battery type. Each element in the list corresponds to a compartment and can be:

        - True if the compartment is occupied
        - False if the compartment is unoccupied
        - None if the compartment does not exist (i.e., is None)

        Args:
            battery_type (str): The type of battery whose compartments to check.

        Returns:
            A list of bool or None indicating the occupation status of each compartment.
        """

        __compartments = self._by_battery_type[battery_type]
        __ret_list = []
        for compartment in __compartments:
            if compartment:
                __ret_list.append(
                    Locks.is_present(compartment.door, compartment.pos)
                )  # returns True or False
            else:  # element/ compartment is None
                __ret_list.append(None)

        return __ret_list

    ########## locking methods via RFID Reader and smartcards ##########
    def rfid_lock(self, battery_type: str, index: int, card_uid: str) -> bool:
        """
        Locks a compartment of the specified battery type at the specified
        index using a scanned smartcard, to connect the door with the
        card UID for later authentication (unlock door).

        Args:
            battery_type (str): The type of battery whose compartment to lock.
            index (int): The index of the compartment to lock.
            card_uid (str): The UID of the inserted smartcard.

        Returns:
            True if the compartment is successfully locked, False otherwise.
        """

        # get the corresponding compartment
        _compartment = self._by_battery_type[battery_type][index]
        if Locks.add_lock(_compartment.door, _compartment.pos, RFIDLock(card_uid)):
            Hardware.rotate_to_position_bridge(_compartment.pos)
            Hardware.open_door_bridge(_compartment.door)
            return True
        return False

    def rfid_unlock(self, battery_type: str, index: int, card_uid: str) -> bool:
        """
        Unlocks a compartment of the specified battery type at the specified
        index using a scanned smartcard UID.
        For a successful unlock, the UID needs to match the UID from the
        locking process

        Args:
            battery_type (str): The type of battery whose compartment to unlock.
            index (int): The index of the compartment to unlock.
            card_uid (str): The UID of the inserted smartcard.

        Returns:
            bool: True if the compartment is successfully unlocked and opened,
                  False otherwise.
        """

        # get the corresponding compartment
        _compartment = self._by_battery_type[battery_type][index]
        if Locks.attempt_unlock_and_remove(_compartment.door, _compartment.pos, card_uid):
            Hardware.rotate_to_position_bridge(_compartment.pos)
            Hardware.open_door_bridge(_compartment.door)
            return True
        return False


Compartments: _Compartments = _Compartments()  # this instance gets called in BackendBridge.py
