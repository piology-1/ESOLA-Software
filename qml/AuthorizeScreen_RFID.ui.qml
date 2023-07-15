import QtQuick 2.15
import QtQuick.Timeline 1.0

ScreenCommon {
    id: root

    signal scanConfirmed
    visible: true
    caption.visible: false

    Text {
        id: bottomText
        y: 58
        height: 100
        text: "Infotext"
        anchors.bottom: parent.bottom
        font.pixelSize: 64
        horizontalAlignment: Text.AlignHCenter
        anchors.horizontalCenterOffset: 0
        anchors.bottomMargin: 524
        Connections {
            target: bottomText
        }
        anchors.horizontalCenter: parent.horizontalCenter
        font.family: Constants.fontFamily
    }

    Image {
        id: image
        x: 305
        y: 180
        width: 671
        height: 421
        source: "../images/bsp_ausweis.jpg" // photo_2023-05-06_09-57-35
        transformOrigin: Item.Center
        clip: false
        scale: 0.6
        fillMode: Image.PreserveAspectFit
    }

    TextButton {
        id: textButton
        x: 442
        y: 550
        text: "Karte scannen"

        Connections {
            target: textButton
            function onClicked(){
                scanConfirmed()
            } 
        }
    }

    Item {
        id: __materialLibrary__
    }

    states: [
        State {
            name: "deposit"

            PropertyChanges {
                target: bottomText
                y: 33
                text: "RFID-Karte innerhalb 10 s an \n das Lesegerät legen und 'scannen'!"
                anchors.horizontalCenterOffset: 11
                anchors.bottomMargin: 547
                //Qt.format("RFID-Karte innerhalb %.1f an das Lesegerät anlegen!", Constants.card_insert_timeout)
            }
        },
        State {
            name: "retrieve"

            PropertyChanges {
                target: bottomText
                text: "RFID-Karte innerhalb 10 s an \n das Lesegerät legen und 'scannen'!" // und RFID-Karte \n innerhalb 10 s an das Lesegerät legen!" // "RFID-Karte innerhalb 10 s \n an das Lesegerät anlegen!"
            }
        },
        State {
            name: "noPermission"
            PropertyChanges {
                target: bottomText
                y: 11
                text: qsTr("<b>Invalide Karte erkannt!</b> \n Zugriff auf das Fach verweigert.") // "Nice try, aber du hast mit dieser Karte \n keinen Zugriff auf dieses Fach 😉"
            }
        }
    ]
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.66;height:680;width:1280}
}
##^##*/

