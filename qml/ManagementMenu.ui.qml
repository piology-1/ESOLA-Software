import QtQuick 2.15

ScreenCommon {
    property alias loeschenAdmin: loeschenAdmin
    property alias registerAdmin: registerAdmin
    property alias registerUser: registerUser
    property alias loeschenUser: loeschenUser

    caption.text: qsTr("Was möchten Sie tun?")

    BigButton {
        id: registerAdmin
        x: 21
        y: 238
        width: 250
        height: 250
        text: "Admin registrieren"
        iconSource: "../images/admin.png"
    }

    BigButton {
        id: loeschenAdmin
        x: 349
        y: 238
        width: 250
        height: 250
        text: "Admin löschen"
        iconSource: "../images/admin_fail.png"
    }

    BigButton {
        id: registerUser
        x: 678
        y: 238
        width: 250
        height: 250
        text: "User registrieren"
        iconSource: "../images/user.png"
    }

    BigButton {
        id: loeschenUser
        x: 1006
        y: 238
        width: 250
        height: 250
        text: "User löschen"
        iconSource: "../images/user_fail.png"
    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:0.66}
}
##^##*/

