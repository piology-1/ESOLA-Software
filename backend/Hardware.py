class _Hardware:
    """
    The Hardware class manages the assignment of the hardware,
    depending on the device the code is currently running on.

    Attributes:
    -----------
        None
    
    Instance Variables:
    -------------------
    _impl_hardware (object):
        An object of the RPiHardware or MockHardware class, initialized 
        based on the type of device where the code is running.
    """
    

    def __init__(self) -> None:
        """
        Try to initialize the Raspberry Pi hardware via the
        RPiHardware module and the RPiHardware class.
        If this fails, initialize a mock Hardware via the
        MockHardware module and the MockHardware class.

        Usually this Code is running on the Raspberry Pi.
        So the Hardware will be initialized as RPiHardware.
        If you run this code just on your PC, there is no Raspberry Pi
        you can initialize.
        So you create a mock Hardware, to test the code.

        Returns: 
            None
        """

        try:
            from .RPiHardware import RPiHardware
            self._impl_hardware = RPiHardware()
        except:
            from .MockHardware import MockHardware
            self._impl_hardware = MockHardware()

    def open_door_bridge(self, door) -> None:
        """
        Open the door for a compartment by calling the method from the 
        initialized hardware class (either RPiHardware or MockHardware)
        
        NOTE:
        The name of this method is redundant to the Methods in the
        MockHardware- and RPiHardware class.

        Args:
            door (int): The index of the door to open.

        Returns:
            None
            Actually, don't know why this method returns something...
            Not implemented in the read Hardware class.
        """

        return self._impl_hardware.open_door(door)

    def rotate_to_position_bridge(self, pos) -> None:
        """
        Rotate to a certain position, calling the method from
        the initialized hardware class (either RPiHardware
        or MockHardware).

        NOTE:
        The name of this method is redundant to the Methods in the
        MockHardware- and RPiHardware class.
        
        Args:
            door (int): The position of the tower to which to rotate.

        Returns:
            None
            Actually, don't know why this method returns something...
            Not implemented in the read Hardware class.
        """

        return self._impl_hardware.rotate_to_position(pos)


Hardware: _Hardware = _Hardware()
