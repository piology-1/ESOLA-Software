import QtQuick 2.15

ScreenCommon {
    property alias einlagern: einlagern
    property alias entnehmen: entnehmen
    property alias registrieren: registrieren

    caption.text: qsTr("Was möchten Sie tun?")

    BigButton {
        id: einlagern
        y: 190
        width: 300
        text: "Einlagern"
        anchors.left: parent.left
        anchors.leftMargin: 86
        iconSource: "../images/einlagern.png"
    }

    BigButton {
        id: entnehmen
        x: 490
        y: 190
        width: 300
        text: "Entnehmen"
        anchors.right: parent.right
        anchors.rightMargin: 490
        iconSource: "../images/entnehmen.png"
    }

    BigButton {
        id: registrieren
        x: 877
        y: 190
        width: 300
        height: 300
        text: "Benutzerverwaltung"
        anchors.right: parent.right
        iconSource: "../images/register.png"
        anchors.rightMargin: 81
    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:0.66}
}
##^##*/

