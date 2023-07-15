import QtQuick 2.15
import QtQuick.Timeline 1.0

Item {
    id: root
    width: Constants.width
    height: Constants.height
    state: "collapsed"

    Rectangle {
        id: bgDarken
        x: 0
        y: 0
        width: root.width
        height: root.height
        color: "#000000"
        opacity: 0

        MouseArea {
            id: mouseAreaBg
            anchors.fill: parent

            Connections {
                function onClicked(mouse) {
                    root.state = "collapsed"
                }
            }
        }
    }

    Rectangle {
        id: help
        x: 1092
        y: 13
        width: 92
        height: 92
        color: "#b3b3b3"
        clip: true
        radius: 46
        border.color: "#858585"
        border.width: 2
        anchors.right: parent.right
        anchors.rightMargin: 125

        Item {
            id: helpText
            x: 52
            width: 926
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.topMargin: 60

            Text {
                id: text1
                color: "#000000"
                textFormat: Text.StyledText
                text: "text1"
                anchors.left: parent.left
                anchors.right: parent.right
                wrapMode: Text.Wrap
                anchors.leftMargin: 0
                anchors.rightMargin: 0
                font.pixelSize: 36
                font.family: Constants.fontFamily
            }

            Text {
                id: text2
                y: 135
                anchors.top: text1.bottom
                anchors.topMargin: 20
                color: "#000000"
                textFormat: Text.StyledText
                text: "text2"
                anchors.left: parent.left
                anchors.right: parent.right
                wrapMode: Text.Wrap
                anchors.rightMargin: 0
                anchors.leftMargin: 0
                font.pixelSize: 36
                font.family: Constants.fontFamily
            }

            Text {
                id: text3
                y: 375
                anchors.top: text2.bottom
                anchors.topMargin: 20
                color: "#000000"
                textFormat: Text.StyledText
                text: "text3"
                anchors.left: parent.left
                anchors.right: parent.right
                wrapMode: Text.Wrap
                anchors.rightMargin: 0
                anchors.leftMargin: 0
                font.pixelSize: 36
                font.family: Constants.fontFamily
            }
        }

        MouseArea {
            id: mouseAreaHelp
            anchors.fill: parent
        }
    }

    Timeline {
        id: timeline
        enabled: true
        startFrame: 0
        endFrame: 900
        currentFrame: 900

        KeyframeGroup {
            target: help
            property: "width"
            Keyframe {
                easing.type: Easing.InOutCubic
                value: 1030
                frame: 840
            }

            Keyframe {
                value: 92
                frame: 0
            }
        }

        KeyframeGroup {
            target: help
            property: "height"
            Keyframe {
                easing.type: Easing.InOutCubic
                value: 600
                frame: 900
            }

            Keyframe {
                value: 92
                frame: 150
            }

            Keyframe {
                value: 92
                frame: 0
            }
        }

        KeyframeGroup {
            target: bgDarken
            property: "opacity"
            Keyframe {
                easing.type: Easing.OutCubic
                frame: 650
                value: 0.6
            }

            Keyframe {
                frame: 150
                value: 0
            }

            Keyframe {
                frame: 0
                value: 0
            }
        }

        KeyframeGroup {
            target: helpText
            property: "opacity"
            Keyframe {
                easing.type: Easing.InSine
                frame: 900
                value: 1
            }

            Keyframe {
                frame: 0
                value: 0
            }

            Keyframe {
                frame: 450
                value: 0
            }
        }
    }

    states: [
        State {
            name: "collapsed"

            PropertyChanges {
                target: timeline
                currentFrame: 0
            }

            PropertyChanges {
                target: mouseAreaBg
                enabled: false
            }
        },

        State {
            name: "home"

            PropertyChanges {
                target: text1
                text: qsTr("<b>Willkommen bei der DHBW Solartankstelle!</b>")
            }

            PropertyChanges {
                target: text2
                text: qsTr("Hier können Sie mit dem <b>Einlagern</b>-Button einen E-Bike-Akku in der Station aufladen lassen. Dabei muss ein DHBW Ausweis an das Lesegerät gehalten werden, um Ihren Akku vor fremdem Zugriff zu schützen.")
            }

            PropertyChanges {
                target: text3
                text: qsTr("Sie können ihn dann später mit dem <b>Entnehmen</b>-Button gegen erneutes Hinalten des Ausweises wieder abholen.")
            }
        },

        State {
            name: "batterytype"

            PropertyChanges {
                target: text1
                text: qsTr("<b>Akkuauswahl</b>")
            }

            PropertyChanges {
                target: text2
                text: qsTr("Um Ihnen das passende Ladegerät für Ihren Fahrradakku zur Verfügung zu stellen, benötigen wir die Angabe des Herstellers Ihres Akkus. Mit Klick auf den jeweiligen Hersteller gelangen Sie zur Fachauswahl.")
            }

            PropertyChanges {
                target: text3
                text: ""
            }
        },

        State {
            name: "compartment"

            PropertyChanges {
                target: text1
                text: qsTr("<b>Fachauswahl</b>")
            }

            PropertyChanges {
                target: text2
                text: qsTr("Wählen Sie hier ein verfügbares Fach aus. Nicht verfügbare Fächer sind ausgegraut und können nicht ausgewählt werden. Mit der Fachnummer und der im nächsten Schritt hinterlegten PIN können Sie den Akku wieder entnehmen.")
            }

            PropertyChanges {
                target: text3
                text: qsTr("Es ist geplant, im Inneren der Anlage einen Drehturm nachzurüsten, sodass in Zukunft mehrere Fächer pro Tür verfügbar sein werden.")
            }
        },
        State {
            name: "authorizeRFID"
            PropertyChanges {
                target: text1
                text: qsTr("<b>DHBW-Ausweis Entsperrung</b>")
            }

            PropertyChanges {
                target: text2
                text: "Damit Ihr Akku vor fremdem Zugriff geschütz ist, wird das Fach mit Ihrer einzigartigen und eindeutigen DHBW-Ausweis Karte geschlossen."
            }

            PropertyChanges {
                target: text3
                text: "Sollten Sie Probleme bei diesem Prozess haben, wenden Sie sich bitte an Herrn Arnold:<br>Telefon: 07541/2077225<br>E-Mail: arnold@dhbw-ravensburg.de"
            }
        },
        State {
            name: "errorcase"

            PropertyChanges {
                target: text1
                text: qsTr("<b>Fehler</b>")
            }

            PropertyChanges {
                target: text2
                text: "Ein Fehler während des Lesevorgangs ist aufgetreten. Dabei kann die Ursache mehrere Gründe haben"
            }

            PropertyChanges {
                target: text3
                text: "Die genaue Fehlermeldung sollte im Fenster angezeigt werden. Sollte auch nach mehrmaligen Versuchen eine Fehlermeldung auftauchen, melden Sie sich bitte bei Herrn Arnold:\nTelefon: 07541/2077225\n E-Mail: arnold@dhbw-ravensburg.de"
            }
        },
        State {
            name: "managementMenu"

            PropertyChanges {
                target: text1
                text: qsTr("<b>Benutzerkontenverwaltung</b>")
                font.bold: true
            }

            PropertyChanges {
                target: text2
                text: "In der Benutzerkontenverwaltung können Sie sich einen Zugriff auf die Schließfächer einrichten. Um Zugriff auf die Ladestation zu erlangen brauchen Sie eine Admin Ausweiskarte."
            }

            PropertyChanges {
                target: text3
                text: "Diese ist bei Prof. Dr. Frank :\n\nTelefon: 07541/2077139\n\n E-Mail: t.frank@dhbw-ravensburg.de\n\n oder Herrn Arnold:\n\nTelefon: 07541/2077225\n\n E-Mail: arnold@dhbw-ravensburg.de\n\nabzuholen" // besitzt. Mit dieser kann ein neues Benutzerkonto erstellt werden."
            }
        }
    ]

    transitions: [
        Transition {
            from: "collapsed"
            to: "*"
            reversible: true
            PropertyAction {
                property: "text"
            }
            PropertyAnimation {
                property: "currentFrame"
                duration: 900
            }
        }
    ]
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.75}
}
##^##*/

