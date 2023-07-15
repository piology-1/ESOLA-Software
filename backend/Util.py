""" Helper Module. """


import os
import sys


_datadir = None


def datadir() -> str:
    """
    Return the path to the current main directory, where all the files are located.
    
    This function returns a string representing the path to the current main directory,
    where all the files are located.
    The first time the function is called, it tries to determine the path using the '__main__' module;
    if that fails, the current working directory (cwd) is used instead.

    Returns:
        str: The path to the current main directory, where all the files are located.
    """

    global _datadir
    if _datadir is None:
        try:
            _datadir = os.path.dirname(sys.modules['__main__'].__file__)
            # print("try block: "+_datadir)  # Debug purposes
        except:
            _datadir = os.getcwd()  # returns current working directory (cwd)
            # print("except block: "+_datadir)  # Debug purposes
    return _datadir


# sys.modules returns a dictionary with a module as a key and the Path as the value (https://docs.python.org/3/library/sys.html)
# returns the path, where the file is located, which calls the function from the beginning (Path of Directory, where gui_main.py is located)
