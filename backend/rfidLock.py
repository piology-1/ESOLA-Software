from .Lock import Lock


class RFIDLock(Lock):
    """
    The RFIDLock class inherits from Lock class and manages the card UID for each Lock/ door.
    
    Attributes:
    -----------
        None
    
    Instance Variables:
    -------------------
    __card_uid (str):
        The unique identifier (UID) of the card associated with this Lock.
    """

    def __init__(self, card_uid: str) -> None:
        """
            Construct a new 'RFIDLock' object with the provided card UID.

        Args:
            card_uid (str): The unique identifier (UID) of the card associated with this lock.
            
        Returns:
            None
        """

        self.__card_uid: str = str(card_uid)

    @classmethod
    def from_dict(cls, _dict):
        """
        Constructs a new 'RFIDLock' object from a given dictionary.

        Args:
            _dict (dict): A dictionary containing the 'card_uid' key
                          corresponding to a string representation of
                          the card UID associated with the lock.

        Returns:
            RFIDLock: A new RFIDLock object initialized with the provided card UID.
        """

        uid: str = _dict["card_uid"]
        return RFIDLock(card_uid=uid)

    def _to_dict(self) -> dict:
        """
        Converts the 'RFIDLock' object to a dictionary.

        This method returns a dictionary containing the necessary information to recreate the 'RFIDLock' object.
        The dictionary contains a single key 'card_uid' which corresponds to a string representation 
        of the card UID associated with the lock.

        Returns:
            dict: A dictionary containing the necessary information to recreate the 'RFIDLock' object.
        """

        return {
            "card_uid": self.__card_uid
        }

    def attempt_unlock(self, key: str) -> bool:
        """
        Attempts to unlock the 'RFIDLock' object using a provided key.

        This method compares the `self.__card_uid` with a string representation of the provided 
        key. If the two match, this method will return True indicating that the lock has been 
        successfully unlocked. If they do not match, this method will return False.

        Args:
            key (str): The inserted key with which to try to unlock the lock/door.
                       In the past, this was a four digit code, now its the card UID.

        Returns:
            bool: True if the lock was successfully unlocked, False otherwise.
        """

        return self.__card_uid == str(key)
