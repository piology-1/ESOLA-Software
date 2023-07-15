class Lock:
    """
    A Lock object for a door.

    Each lock has its own dictionary with specific contents,
    consisting of a 'type' key and a 'card_uid' key:

    Ex.:
        {
            'typ': 'card_uid',
            'card_uid': 'AA BB CC 11'
        }

    Attributes:
    -----------
    _types (dict):
        are used to store the supported lock types

    _names (dict):
        are used to store the supported lock names
    
    Instance Variables:
    -------------------
        None

    NOTE:
    For methods decorated with @classmethod, the class (cls) is 
    used as the first argument instead of an instance (self).
    """

    _types = None
    _names = None

    @classmethod
    def _init_types(cls) -> None:
        """
        Initializes the supported lock types and their names.

        Args:
            cls (Lock): The Lock class.

        Returns:
            None.
        """

        # Wird von __init__ in Locks.py aufgerufen,
        if not cls._types:
            from .rfidLock import RFIDLock
            cls._types = {
                "card_uid": RFIDLock
            }
            cls._names = {t: n for n, t in cls._types.items()}

    @classmethod
    def from_dict(cls, _dict):
        """
        Create a new Lock object from the given dictionary.

        Args:
            _dict (dict): A dictionary representing a specific lock/door, with keys 
                           'type' and 'card_uid' indicating its type and card UID 
                           respectively. 

                           Example:
                           {
                               'type': 'card_uid',
                               'card_uid': 'AA BB CC 11'
                           }

        Returns:
            Depending on the try/except statement, either a new `RFIDLock`
            object or None.
        """

        try:
            if _dict['type'] in cls._types:
                return cls._types[_dict['type']].from_dict(_dict)
            else:
                raise NotImplementedError("lock type '%s'" % _dict['type'])
        except KeyError:
            raise ValueError("missing type")

    def to_dict(self) -> dict:
        """
        Converts a dictionary with the format {'type': 'card_uid'} into a dictionary 
        with the format {'type': 'card_uid', 'card_uid': '__code__'}, where __code__
        is the card UID used to lock the door.

        Example:
            {'type': 'card_uid'}  =>  {'type': 'card_uid', 'card_uid': '11 22 33'}

        Args:
            None

        Returns:
            A dictionary with 'type' and 'card_uid' as the keys of the dictionary.
        """

        _dict = {
            'type': Lock._names[type(self)]
        }
        _dict.update(self._to_dict())
        return _dict

    def _to_dict(self) -> None:
        """
        This method is not yet implemented.

        Returns:
            None
        """

        raise NotImplementedError

    def attempt_unlock(self, key:str) -> None:
        """
        This method is not yet implemented.
        Attempt to unlock the object with the given key.

        Args:
            key (str): The key to use for unlocking

        Returns:
            None
        """

        raise NotImplementedError
