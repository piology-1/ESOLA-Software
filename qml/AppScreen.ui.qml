import QtQuick 2.15
import QtQuick.Window 2.15

Rectangle {
    id: root
    width: Constants.width
    height: Constants.height
    color: Constants.backgroundColor

    state: "welcome"
    property alias managementMenu: managementMenu
    property alias userManagement: userManagement
    property alias standbyResetMouseArea: standbyResetMouseArea
    property alias error_caseForm: error_caseForm
    property alias authorizeScreen_RFID: authorizeScreen_RFID
    property alias topBar: topBar
    property alias button_back: button_back
    property alias welcomeScreen: welcomeScreen
    property alias homeScreen: homeScreen
    property alias batteryTypeScreen: batteryTypeScreen
    property alias compartmentScreen: compartmentScreen
    property alias finishScreen: finishScreen
    property alias authorizeScreen: authorizeScreen

    TopBar {
        id: topBar
        x: 0
        y: 0
        z: 10
        state: root.state
    }

    ImageButton {
        id: button_back
        x: 16
        width: 96
        height: 96
        anchors.top: topBar.bottom
        source: "../images/button_back.png"
        anchors.topMargin: 12
    }

    WelcomeScreen {
        id: welcomeScreen
        x: 0
        y: 0
        visible: false
    }

    HomeScreen {
        id: homeScreen
        visible: false
        x: 0
        y: Constants.topBarHeight
    }

    BatteryTypeScreen {
        id: batteryTypeScreen
        visible: false
        x: 0
        y: Constants.topBarHeight
    }

    CompartmentScreen {
        id: compartmentScreen
        x: 0
        y: Constants.topBarHeight
        visible: false
    }

    AuthorizeScreen {
        id: authorizeScreen
        x: 0
        y: Constants.topBarHeight
        visible: false
    }

    AuthorizeScreen_RFID {
        id: authorizeScreen_RFID
        x: 0
        y: Constants.topBarHeight
        visible: false
    }

    FinishScreen {
        id: finishScreen
        x: 0
        y: 0
        visible: false
    }

    Error_caseForm {
        id: error_caseForm
        visible: false
    }

    UserManagement {
        id: userManagement
        visible: false
    }

    ManagementMenu {
        id: managementMenu
        visible: false
    }

    MouseArea {
        id: standbyResetMouseArea
        anchors.fill: parent
        cursorShape: Qt.UpArrowCursor
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
        z: 100
        visible: true
    }

    states: [
        State {
            name: "welcome"

            PropertyChanges {
                target: topBar
                visible: false
            }

            PropertyChanges {
                target: welcomeScreen
                visible: true
            }

            PropertyChanges {
                target: button_back
                visible: false
            }
        },
        State {
            name: "home"

            PropertyChanges {
                target: homeScreen
                visible: true
            }

            PropertyChanges {
                target: button_back
                visible: false
            }
        },
        State {
            name: "batterytype"
            PropertyChanges {
                target: batteryTypeScreen
                visible: true
            }
            PropertyChanges {
                target: standbyResetMouseArea
                visible: true
            }
        },
        State {
            name: "compartment"

            PropertyChanges {
                target: batteryTypeScreen
                visible: false
            }

            PropertyChanges {
                target: compartmentScreen
                visible: true
            }
        },
        State {
            name: "authorize"

            PropertyChanges {
                target: authorizeScreen
                visible: true
            }
        },
        State {
            name: "finish"

            PropertyChanges {
                target: topBar
                visible: false
            }

            PropertyChanges {
                target: finishScreen
                visible: true
            }

            PropertyChanges {
                target: button_back
                visible: false
            }

        },
        State {
            name: "occupied"

            PropertyChanges {
                target: error_caseForm
                visible: false
            }

        },
        State {
            name: "authorizeRFID"

            PropertyChanges {
                target: authorizeScreen_RFID
                visible: true
            }

            PropertyChanges {
                target: standbyResetMouseArea
                visible: true
            }
        },
        State {
            name: "errorcase"

            PropertyChanges {
                target: error_caseForm
                x: 0
                y: 126
                visible: true
            }

            PropertyChanges {
                target: button_back
                visible: false
            }
        },
        State {
            name: "userManagement"          

            PropertyChanges {
                target: userManagement
                x: 0
                y: 120
                visible: true
            }

            PropertyChanges {
                target: button_back
                visible: false
            }
        },
        State {
            name: "managementMenu"

            PropertyChanges {
                target: managementMenu
                x: 0
                y: 126
                visible: true
            }
        }
    ]
}
