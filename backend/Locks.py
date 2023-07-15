import json
from .Lock import Lock
from .rfidLock import RFIDLock
from . import Util


class _Locks:
    """
    The Locks class manages the use of all locks.

    It handles creation of new locks as well as restoration
    of previously existing locks from the `locks.json` file.

    Attributes:
    -----------
        None
    
    Instance Variables:
    -------------------
    _persist_file (str):
        Path to the file where lock data will persist.

    _persistence_paused (bool):
        Flag indicating if persistence functionality is paused.
        
    _locks (dict):
        A dictionary containing data regarding each lock.
        Example:
            {   
                1: {0: <backend.PinLock.PinLock object at 0x00000159FF138070>},
                2: {0: <backend.PinLock.PinLock object at 0x00000159FF139720>},
                3: {0: <backend.PinLock.PinLock object at 0x00000159FF139750>},
                4: {0: <backend.PinLock.PinLock object at 0x00000159FF1396C0>}
            }
    """

    def __init__(self) -> None:
        """
        Construct a new '_Locks' object and initialize it through the '_init_type()'
        classmethod in 'Lock.py'. Restore lock data from the `locks.json` file and
        make its content/ data available in the program code.

        Args:
            None

        Returns:
            None
        """

        Lock._init_types()  # pass the Lock class as an argument --> @classmethod
        self._persist_file: str = Util.datadir() + '/locks.json'
        self._persistence_paused: bool = False
        self._locks: dict = {}
        self._disk_restore()

    def _disk_restore(self) -> None:
        """
        Try to restore lock data from the `self._persist_file` file, and
        load its contents into the `_locks` dictionary. The stored data
        will be available in the program code.

        Args:
            None
        
        Returns:
            None
        """

        try:
            with open(self._persist_file) as f:
                for door_numb, locks in json.load(f).items():
                    door_numb = int(door_numb)
                    self._locks[door_numb] = {}
                    for tower_pos, lock_dict in locks.items():
                        # print("Lock:"+str(lock_dict))
                        self._locks[door_numb][int(tower_pos)] = Lock.from_dict(
                            dict(lock_dict))
        except FileNotFoundError:
            pass

    def _disk_persist(self) -> None:
        """
        Write all the data in self.locks into the locks.json file.
        This way, the data is stored and available when the program runs again.

        Args:
            None
        
        Returns:
            None
        """

        with open(self._persist_file, 'w') as f:
            json.dump(self._locks, f, indent=2, default=lambda l: l.to_dict())
            f.write('\n')

    def _on_modified(self) -> None:
        """
        Call the _disk_persist() method to write the data into the locks.json file,
        if self._persistence_paused is not False.

        Args:
            None

        Returns:
            None
        """

        if not self._persistence_paused:
            self._disk_persist()

    def is_present(self, door_numb: int, tower_pos: int) -> bool:
        """
        Determines if the value of self._locks at the key position
        _locks[door_numb][tower_pos] is a valid PinLock object.
        The method is called in Compartments.py.

        Args:
            door_numb (int): The index of the door/ lock.
            tower_pos (int): The position of the tower.

        Returns:
            bool: True if the lock is present/ available, False otherwise.
        """

        try:
            return bool(self._locks[door_numb][tower_pos])
        except:
            return False

    def attempt_unlock_and_remove(self, door_numb: int, tower_pos: int, key: any) -> bool:
        """
        Attempts to unlock and remove a lock using the attempt_unlock() and remove() methods.
        Updates the locks.json file using the _on_modified() method.

        Args:
            door_numb (int): The index of the door/lock.
            tower_pos (int): The position of the tower.
            key (any): The key (card UID?) required to unlock the lock.

        Returns:
            bool: True if the lock was successfully unlocked and removed, False otherwise.
        """

        self._persistence_paused = True
        success = self.attempt_unlock(door_numb, tower_pos, key)
        if success:
            self.remove(door_numb, tower_pos)
        self._persistence_paused = False
        self._on_modified()
        return success

    def attempt_unlock(self, door_numb: int, tower_pos: int, key: any):
        """
        Attempts to unlock a Lock using the attempt_unlock() method in
        Lock.py or rfidLock.py.

        Args:
            door_numb (int): The index of the door/ lock.
            tower_pos (int): The position of the tower.
            key (any): The key (card UID?) required to unlock the lock.

        Returns:
            bool: True if the lock was successfully unlocked, False otherwise.
        """

        try:
            return self._locks[door_numb][tower_pos].attempt_unlock(key)
        except KeyError:
            return False

    def remove(self, door_numb: int, tower_pos: int) -> bool:
        """
        Removes a lock from the self._locks dictionary and updates
        the changes in the locks.json file via the _on_modified() method.

        Args:
            door_numb (int): The index of the door/ lock.
            tower_pos (int): The position of the tower.

        Returns:
            bool: True if the lock was successfully removed, False otherwise.
        """

        try:
            del (self._locks[door_numb][tower_pos])
            if not self._locks[door_numb]:
                del (self._locks[door_numb])
            self._on_modified()
            return True
        except KeyError:
            return False

    def add_lock(self, door_numb: int, tower_pos: int, lock: RFIDLock) -> bool:
        """
        Adds a lock to the self._locks dictionary and updates the changes
        via the _on_modified() method.

        Args:
            door_numb (int): The index of the door/ lock.
            tower_pos (int): The position of the tower.
            lock (RFIDLock object): The Lock object to be added.
                                    In the past PinLock now RFIDLock.

        Returns:
            bool: True if the lock was successfully added, False otherwise.
        """
        

        if not door_numb in self._locks:
            self._locks[door_numb] = {}  # nested locks dictionary
        if tower_pos in self._locks[door_numb]:
            return False
        self._locks[door_numb][tower_pos] = lock  # add the lock
        self._on_modified()  # update locks.json
        return True


Locks: _Locks = _Locks()
