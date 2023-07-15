#!/usr/bin/env python3

# --> make sure, that this gui_main.py file is an executable script

"""
This Module is the main module, from where the program and the GUI is launched.
Here the QML data is loaded.
"""

import os
import sys
from pathlib import Path
from PySide2.QtCore import QObject, QUrl

from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtGui import QGuiApplication

# import the instance from BackendBridge
from backend.BackendBridge import BackendBridge

# getting the path of the current main directory with all the files
CURRENT_DIRECTORY = Path(__file__).resolve().parent

def initQML():
    """
    From this module you can start the program.
    It will initialize the QML and start the Backend for controling the System.
    """

    app = QGuiApplication(sys.argv)  # Create an App Oject
    qmlengine = QQmlApplicationEngine()  # Create a qml engine
    qmlengine.quit.connect(app.quit)

    # whole path to Solartankstelle.qml
    main_qml_file_path = os.fspath(CURRENT_DIRECTORY / "Solartankstelle.qml")
    file_url = QUrl.fromLocalFile(main_qml_file_path)
 
    # Load QML Data from "Solartankstelle.qml"
    qmlengine.load(file_url)

    # Returns a list of all the root objects instantiated by the QQmlApplicationEngine
    root_objects = qmlengine.rootObjects()
    if len(root_objects) == 0:  # check whether the list of rootObjects is empty or not
        # print("Failed to load qml file:\t" + main_qml_file_path)
        quit()

    # print(main_qml_file_path + " loaded sucessfully")

    # getting the rootObject; type: QObject
    qmlApplicationWindow = root_objects[0]

    qmlApp = qmlApplicationWindow.findChild(
        QObject, "app")  # Find the target object

    # Set the propertys with backendBridge
    qmlApp.setProperty('backendBridge', BackendBridge)

    sys.exit(app.exec_())  # exit the application


# Execute the code only if the file was run directly, and not imported
if __name__ == "__main__":
    BackendBridge.start_rfid_reader_monitoring()
    initQML()
    BackendBridge.end_rfid_reader_monitoring()
