
/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick 2.15
import QtQuick.Timeline 1.0

// import QtQuick.Studio.Components 1.0
ScreenCommon {
    id: root

    caption.visible: false

    signal cancel
    signal retry
    visible: true
    caption.color: "#ffffff"

    Text {
        id: bottomText
        y: 58
        text: qsTr("<b>Scan fehlgeschlagen<b>")
        anchors.bottom: parent.bottom
        font.pixelSize: 64
        horizontalAlignment: Text.AlignHCenter
        anchors.horizontalCenterOffset: 0
        anchors.bottomMargin: 524
        anchors.horizontalCenter: parent.horizontalCenter
        font.family: Constants.fontFamily
    }

    TextButton {
        id: textButton
        x: 130
        y: 500
        visible: false
        text: "Erneut versuchen"

        Connections {
            target: textButton
            function onClicked(mouse) {
                root.retry()
            }
        }
    }

    Text {
        id: bottomText1
        y: 291
        text: "Errormessage"
        anchors.bottom: parent.bottom
        font.pixelSize: 64
        horizontalAlignment: Text.AlignHCenter
        anchors.bottomMargin: 291
        anchors.horizontalCenter: parent.horizontalCenter
        font.family: Constants.fontFamily
        anchors.horizontalCenterOffset: 1
    }

    TextButton {
        id: textButton1
        x: 730
        y: 500
        text: "Hauptmenü"
        Connections {
            target: textButton1
            function onClicked(mouse) {
                root.cancel()
            }
        }
    }

    states: [
        State {
            name: "NoCardReader"

            PropertyChanges {
                target: bottomText1
                text: "Es konnte keine Verbindung \n zum Lesegerät hergestellt werden"
            }
        },
        State {
            name: "UnsuccessfulUIDCardRead"

            PropertyChanges {
                target: bottomText1
                text: "Fehler beim Lesen der Karte"
            }
        },
        State {
            name: "CardRequestTimeout"

            PropertyChanges {
                target: bottomText1
                y: 291
                text: "Scan Timeout - Karte muss innerhalb 10 s \n an das Lesegreät gehalten werden"
                anchors.horizontalCenterOffset: 1
                anchors.bottomMargin: 291
            }
        },
        State {
            name: "NoCard"

            PropertyChanges {
                target: bottomText1
                y: 291
                text: "Keine Karte am Lesegerät erkannt.\n Karte für längeren Zeitraum an Gerät halten"
                horizontalAlignment: Text.AlignHCenter
                anchors.horizontalCenterOffset: 0
                anchors.bottomMargin: 291
            }
        },
        State {
            name: "CardConnection"

            PropertyChanges {
                target: bottomText1
                y: 291
                text: "Verbindungsabbruch zur Karte \n während des Lesens"
                anchors.horizontalCenterOffset: 1
                anchors.bottomMargin: 291
            }
        },
        State {
            name: "UndefinedError"

            PropertyChanges {
                target: bottomText1
                text: "Unspezifischer Error beim Lesen aufgetreten..."
            }
        }
        
        
    ]
}
