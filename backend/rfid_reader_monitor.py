from smartcard.ReaderMonitoring import ReaderMonitor, ReaderObserver
from .rfid_reader import RFIDReader


class _RFIDReaderObserver(ReaderObserver):
    """
    A simple reader observer that is notified when readers
    are added/removed from the system. 

    A running instance of RFIDReader can detect when RFID
    Readers are plugged and unplugged multiple times during
    one run session and will be ready to scan every time it
    gets plugged in again.
    
    Attributes:
    -----------
        None
    
    Instance Variables:
    -------------------
        None
    """

    def update(self, observable: ReaderMonitor, actions: tuple[list[str], list[str]]):
        """
        Sets the corresponding is_available attribute of the RFIDReader object.
        
        Args:
            observable (ReaderMonitor): An instance of ReaderMonitor.
            actions (tuple[list[str], list[str]]): A tuple containing 2 lists of
                                                   added and removed readers.
        
        Returns:
            None
        """

        added_readers, removed_readers = actions
        if added_readers:
            print("Added readers", added_readers)
            RFIDReader.is_available = True
        if removed_readers:
            print("Removed readers", removed_readers)
            RFIDReader.is_available = False


class _ManageReaderMonitoring(object):
    """
    A class that manages RFID Reader monitor.

    Attributes:
    -----------
        None
    
    Instance Variables:
    -------------------
    reader_monitor (ReaderMonitor):
        An instance of ReaderMonitor.
    
    rfid_reader_observer (_RFIDReaderObserver):
        An instance of _RFIDReaderObserver.
    
    """

    def __init__(self) -> None:
        """
        Initializes instances of ReaderMonitor, _RFIDReaderObserver classes.
                
        Args:
            None
        
        Returns:
            None
        """

        self.reader_monitor: ReaderMonitor = ReaderMonitor()
        self.rfid_reader_observer: _RFIDReaderObserver = _RFIDReaderObserver()

    def start(self) -> None:
        """
        Adds an observer to the ReaderMonitor object and starts monitoring.
        
        Args:
            None
        
        Returns:
            None
        """
        # at this point, the update method of the printobserver class gets called
        self.reader_monitor.addObserver(self.rfid_reader_observer)

    def end(self) -> None:
        """
        Deletes the observer from the ReaderMonitor object and ends monitoring.
        
        Args:
            None
            
        Returns:
            None
        """

        # don't forget to remove observer, or the monitor will poll forever...
        self.reader_monitor.deleteObserver(self.rfid_reader_observer)


RFIDReaderManagement: _ManageReaderMonitoring = _ManageReaderMonitoring()