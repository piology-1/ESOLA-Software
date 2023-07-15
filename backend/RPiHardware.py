import threading
import time

import RPi.GPIO as GPIO


class RPiHardware:
    """
    Handles the Hardware, which is responsible for opening and closing the compartments.

    Attributes:
        door_pins (Tuple[int]): A tuple of integers representing the GPIO pins used to
                                open/ lock each of the five compartment doors.
    """

    door_pins = (29, 31, 33, 35, 37)

    def __init__(self) -> None:
        """Constructs a new 'RPiHardware' object.

        Initializes the GPIO pins of the Raspberry Pi and sets the door pins correctly.

        Returns:
            None
        """

        GPIO.setmode(GPIO.BOARD)
        for pin in self.door_pins:
            GPIO.setup(pin, GPIO.OUT)

    def __del__(self) -> None:
        """
        Deletes the pins, which were set by the `__init__()` method.

        Cleans up all the used GPIO pins so that they can be used again.

        Returns:
            None
        """

        GPIO.cleanup(self.door_pins)

    @staticmethod
    def _signal_pulse(gpio_pin: int) -> None:
        """
        Send a signal pulse to the specified Raspberry Pi GPIO Pin.

        Sends a high signal to the specified GPIO pin, waits for 0.2 seconds
        and then sends a low signal to the same pin.

        Args:
            Pin (int): The GPIO Pin number to send the pulse to.

        Returns:
            None.
        """

        GPIO.output(gpio_pin, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(gpio_pin, GPIO.LOW)

    def open_door(self, door_numb: int) -> None:
        """
        Open the specified compartment door.

        This method opens the door of a specified compartment by sending a
        signal pulse to the GPIO Pin connected to the door lock mechanism.

        Args:
            door_numb (int): The index of the compartment door to open.

        Returns:
            None
        """

        pin = self.door_pins[door_numb]
        threading.Thread(target=self._signal_pulse, args=(pin,)).start()

    def rotate_to_position(self, tower_pos: int) -> None:
        """
        Rotate the Tower of the ESOLA to the specified position.
        This method rotates the Tower of the ESOLA to the given position.
        
        Args:
            tower_pos (int): The position to which the Tower should rotate.

        Returns:
            None

        NOTE:
            This method is currently not implemented!
        """

        if tower_pos != 0:
            raise NotImplementedError
