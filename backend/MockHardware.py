class MockHardware:
    """
    A class that aids in developing and debugging hardware-related code. 
    It just has a benefit for developing the code. 
    No actual use for controlling the real/ actual Hardware.

    Attributes:
    -----------
        None
    
    Instance Variables:
    -------------------
        None
    """
   
    def open_door(self, door) -> None:
        """
        Prints debug data when a door is opened.
        
        Args:
            door (int): The number of the door that was opened.
            
        Returns:
            None
        """

        print(f"{door+1}. Tür von oben wurde geöffnet.")

    def rotate_to_position(self, pos) -> None:
        """
        Prints debug data when the tower is rotated.
        
        Args:
            pos (int): The position to which the tower has been rotated.
        
        Returns:
            None
        """
       
        print(f"Turm wurde in Stellung {pos} gedreht.")
