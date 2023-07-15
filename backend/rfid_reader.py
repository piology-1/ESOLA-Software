from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import CardRequestTimeoutException, NoCardException, CardConnectionException
from smartcard.util import toHexString
from smartcard.System import readers
from smartcard.pcsc.PCSCReader import PCSCReader
from smartcard.CardConnectionDecorator import CardConnectionDecorator
from smartcard.PassThruCardService import PassThruCardService

class _SmartCard:
    """
    A class representing a smartcard that can be used to manage and
    validate different aspects, such as the card's UID in hex format.
    
    Attributes:
    -----------
        None
    
    Instance Variables:
    -------------------
    __card_uid (str):
        The unique identifier of the smartcard in hexadecimal format.
    """
   
    def __init__(self, card_uid: str) -> None:
        """
        Initializes the _SmartCard instance with the specified card_uid
        if it's valid.

        Args:
            card_uid (str): The unique identifier of the smartcard in
                            hexadecimal format.

        """

        if self.validate_uid(card_uid):
            self.__card_uid = card_uid

    @staticmethod
    def validate_uid(card_uid: str) -> bool:
        """
        Determines whether the specified card_uid is a valid hexadecimal string.

        Args:
            card_uid (str): The unique identifier of the smartcard.

        Returns:
            bool: True if the specified card_uid is a valid hexadecimal string, 
                  False otherwise.
        """
        
        # remove spaces from string
        uid: str = card_uid.replace(" ", "")
        try:
            int(uid, 16)
        except ValueError:
            return False
        return True


class _RFIDReader(object):
    """
    Represents an RFID Reader that can scan smartcards.

    Attributes:
    -----------
    UID_APDU_HEX_STRING (list[hex]):
        The hex string format of the command to send to the smartcard in
        order to get its UID.
        Refer to ACR122U documentation chapter 4.1 for more information.

    CARD_INSERT_TIMEOUT (int):
        The timeout value for waiting for a smartcard to be inserted.
        Default value is 10 seconds.

        
    Instance Variables:
    -------------------
    __reader_available (bool):
        A flag indicating whether the RFID reader is available for scanning
        smartcards or not.

    __card_uid (str):
        The hexadecimal card UID of the last scanned card.

    __error_message (str):
        The error message of the last scan, if one occurred.
    
    __successfully_read_card (bool):
        A flag indicating whether the last scan was successful (no errors)
        or not.
    """

    # ACR122U documentation chapter 4.1
    UID_APDU_HEX_STRING: list[hex] = [0xFF, 0xCA, 0x00, 0x00, 0x00]
    CARD_INSERT_TIMEOUT: int = 10  # s

    def __init__(self) -> None:
        """
        Initializes a new instance of the RFIDReader class.

        This constructor creates a new ACR122U object and initializes its
        Reader and card connection objects.
        The object is ready to use for reading RFID tags after initialization.

        NOTE:
            ACR122U documentation available here: http://downloads.acs.com.hk/drivers/en/API-ACR122U-2.02.pdf
        
        Args:
            None

        Returns:
            None
            
        """

        # gets set to True in __instantiate_reader, if reader is available
        self.__reader_available: bool = False

        # initialize instance variables
        self.__card_uid: str = ""
        self.__error_message: str = ""
        self.__successfully_read_card: bool = False

        self.connection: CardConnectionDecorator
        self.reader: PCSCReader

        # unpack returned tuple
        self.reader, self.connection = self.__instantiate_reader()

    def __instantiate_reader(self) -> tuple[PCSCReader, CardConnectionDecorator]:
        """
        Instantiate a PCSC Reader and card connection.

        This method attempts to create a new PCSC reader object and a corresponding card connection object.
        If successful, the method sets the variable '__reader_available' to True and returns the Reader
        and card connection objects as a tuple. If unsuccessful, the method sets '__reader_available' to False,
        prints an error message, and returns None for both objects.

        Args:
            None

        Returns:
            A tuple containing the instantiated reader object and card connection object, or None for both.

        Raises:
            None
        """

        try:
            # Get available readers
            available_readers: list[PCSCReader] = readers()

            if len(available_readers) == 0:
                # TODO: what should happen if there are no readers?
                self.__reader_available: bool = False
                print("No readers available")
                return None, None
                # raise Exception("No readers available")

            reader: PCSCReader = available_readers[0]
            # Create card connection object for selected reader
            card_connection: CardConnectionDecorator = reader.createConnection()

            self.__reader_available: bool = True

            # Return reader and card connection as a tuple
            return reader, card_connection

        except Exception as e:
            # catch all other exceptions
            print(f"error: {e} occured while instantiating the reader")
            return None, None

    def scan_card(self) -> None:
        """
            Reads an inserted smartcard via the RFIDReader class and sets the instance variables
            'self.__card_uid', 'self.__error_message' and 'self.__successfully_read_card'.

            If the smartcard is successfully read, the UID of the card is stored in the '__card_uid' attribute 
            and the '__successfully_read_card' variable is set to True.

            If something goes wrong during the reading process, various exceptions are caught,
            each with a specific error message which is stored in the '__error_message' attribute.
            This error message will correspond to the different states (screens and messages) in
            'Error_caseForm.ui.qml'. The backendBridge in App.qml can then use these messages to display
            the appropriate screens for the user.
            The '__successfully_read_card' variable is set to False when an error occurs.

            Returns:
                None
        """
        
        # reset the instance variables
        self.reset_instance_attributes()

        # Check if the reader is available
        if not self.is_available:
            # print("There is no reader available to read a smartcard!")
            self.__error_message = "NoCardReader"
            self.__successfully_read_card = False
            return

        try:
            # Create a CardRequest object with a timeout value and request any card type
            card_request: CardRequest = CardRequest(
                timeout=self.CARD_INSERT_TIMEOUT, cardType=AnyCardType())

            # Wait for the card to be inserted
            print(
                f"insert a card (SIM card if possible) within {self.CARD_INSERT_TIMEOUT}s")
            card_service: PassThruCardService = card_request.waitforcard()

            ### Attach a console tracer to display the card connection status --> just for debug purposes ###
            # card_observer = ConsoleCardConnectionObserver()
            # card_service.connection.addObserver(card_observer)

            # connect to the card to perform transmits
            card_service.connection.connect()

            # disable buzzer sound when card is connected
            card_service.connection.transmit([0xFF, 0x00, 0x52, 0x00, 0x00])

            # Connect to the card and send the UID APDU command
            # with card_service.connection.connect():
            card_response, sw1, sw2 = card_service.connection.transmit(
                self.UID_APDU_HEX_STRING)

            # Check if the response APDU Status words (SW) indicates success
            if sw1 == 0x90 and sw2 == 0x0:
                # card was read successfully --> convert the card_response to a hexadecimal string
                uid: str = toHexString(card_response)
                if _SmartCard.validate_uid(card_uid=uid):
                    self.__card_uid = toHexString(card_response)
                    self.__successfully_read_card = True
                    return
                else:
                    self.__error_message = "SomeError"
                    self.__successfully_read_card = False
                    return

            else:
                # if the response APDU Status words (SW) indicates an unsuccessful card read for the UID
                self.__error_message = "UnsuccessfulUIDCardRead"
                self.__successfully_read_card = False
                return

        except CardRequestTimeoutException:
            print(
                f"Time-out: no card inserted during last {self.CARD_INSERT_TIMEOUT}s")
            self.__error_message = "CardRequestTimeout"
            self.__successfully_read_card = False
            return

        except NoCardException:
            print(f"No card present in the reader")
            self.__error_message = "NoCard"
            self.__successfully_read_card = False
            return

        except CardConnectionException:
            # The card needs to be inserted for about 2-3s so read the UID successfully
            print(f"Error: Unable to connect to the card")
            self.__error_message = "CardConnection"
            self.__successfully_read_card = False
            return

        except Exception as e:
            # catch all other exceptions
            print(f"Error: '{e}' occured while inserting and reading the card")
            self.__error_message = "SomeError"
            self.__successfully_read_card = False
            return

    def reset_instance_attributes(self) -> None:
        """
        Resets the instance variables 'self.__card_uid', 'self.__error_message', and
        'self.__successfully_read_card' to their initial values.
        This is necessary that new cards can be read after another card has been read.
        This ensures that a fresh state is maintained when the method is called again
        to read a new card.

        Returns:
            None
        """

        self.__card_uid: str = ""
        self.__error_message: str = ""
        self.__successfully_read_card = False

    ### getter/ setter methods for the BackendBridge ###
    @property
    def is_available(self) -> bool:
        """
        Getter method to check if the card reader is available.

        Returns:
            bool: True if the card reader is available, False otherwise.
        """
        
        return self.__reader_available
    
    
    @is_available.setter
    def is_available(self, status: bool) -> None:
        """
        Setter method to set the availability status of the card reader.
        This method is used by the '_RFIDReaderObserver' Class in rfid_reader_monitor.py

        Args:
            status (bool): A boolean value indicating the status of the card reader's availability.

        Returns:
            None
        """

        if isinstance(status, bool):
            self.__reader_available = status

    @property
    def get_read_status(self) -> bool:
        """
        Getter method to retrieve the reading status of the last scanned card.

        Returns:
            bool: True if the card was successfully read, False otherwise.
        """
        
        return self.__successfully_read_card

    @property
    def get_card_uid(self) -> str:
        """
        Getter method to retrieve the card's unique identifier.

        Returns:
            str: The unique identifier of the card.
        """

        return self.__card_uid

    @property
    def get_error_message(self) -> str:
        """
        Getter method to retrieve any error message associated with the last card reading process.

        Returns:
            str: An error message, if present, else an empty string.
        """

        return self.__error_message


RFIDReader: _RFIDReader = _RFIDReader()
