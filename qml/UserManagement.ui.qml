

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick 2.15

ScreenCommon {
    id: root

    caption.visible: false

    signal cancel
    signal register
    signal scan_admin
    signal scan_new_user
    signal scan_new_admin
    signal delete_user
    signal delete_admin

    // property string previousState
    TextButton {
        id: textButton
        x: 130
        y: 550
        text: "Karte scannen"

        Connections {
            target: textButton
            function onClicked() {
                if (state == "authorize_admin") {
                    root.scan_admin()
                } else if (state == "authorize_new_user") {
                    root.scan_new_user()
                } else if (state == "authorize_new_admin") {
                    root.scan_new_admin()
                } else if (state == "delete_admin") {
                    root.delete_admin()
                } else if (state == "delete_user") {
                    root.delete_user()
                }
            }
        }
    }

    Text {
        id: text1
        x: 284
        y: 85
        text: qsTr("Unbekannter Nutzer erkannt. \n Möchtenn Sie sich registrieren?")
        font.pixelSize: 40
        horizontalAlignment: Text.AlignHCenter
        anchors.horizontalCenterOffset: 0
        anchors.horizontalCenter: parent.horizontalCenter
        font.family: Constants.fontFamily
    }

    TextButton {
        id: textButton1
        x: 730
        y: 550
        text: "Abbrechen"

        Connections {
            target: textButton1
            function onClicked() {
                root.cancel()
            }
        }
    }

    Image {
        id: image
        x: 455
        y: 117
        width: 370
        height: 467
        source: "../images/anonymous.jpg"
        scale: 0.7
        fillMode: Image.PreserveAspectFit
    }

    Image {
        id: image1
        x: 927
        y: 301
        width: 100
        height: 100
        visible: false
        source: "qrc:/qtquickplugin/images/template_image.png"
        fillMode: Image.PreserveAspectFit
    }
    states: [
        State {
            name: "authorize_admin"

            PropertyChanges {
                target: image
                visible: true
                source: "../images/admin.png"
            }

            PropertyChanges {
                target: text1
                text: qsTr("Administrator Karte anlegen und scannen")
            }

            PropertyChanges {
                target: textButton
                y: 550
                text: "Scan"
            }

            PropertyChanges {
                target: textButton1
                y: 550
            }

            PropertyChanges {
                target: image1
                visible: false
            }
        },

        State {
            name: "authorize_new_user"

            PropertyChanges {
                target: image
                source: "../images/user.png"
            }

            PropertyChanges {
                target: text1
                text: qsTr("Karte des neuen Nutzers anlegen und scannen")
            }

            PropertyChanges {
                target: image1
                visible: false
            }
        },

        /// ERROR CASES \\\
        State {
            name: "InvalidAdminCard"
            PropertyChanges {
                target: image
                visible: true
                source: "../images/admin.png"
            }

            PropertyChanges {
                target: text1
                text: qsTr("<b>Die angelegte Karte hat keine \n Admin Rechte!</b>")
            }

            PropertyChanges {
                target: textButton
                visible: false
            }

            PropertyChanges {
                target: textButton1
                x: 440
                y: 550
                text: "Hauptmenü"
            }

            PropertyChanges {
                target: image1
                x: 489
                y: 268
                width: 281
                height: 206
                visible: true
                source: "../images/kisspng-x-mark-symbol-cross-clip-art-x-mark-5ac194c760ed24.866024191522635975397.png"
            }
        },
        State {
            name: "successfully_added"

            PropertyChanges {
                target: image
                x: 455
                y: 107
                source: "../images/pngwing.com.png"
            }

            PropertyChanges {
                target: text1
                text: qsTr("<b>Die Karte wurde \n erfolgreich hinzugefügt!</b>")
            }

            PropertyChanges {
                target: textButton
                visible: false
            }

            PropertyChanges {
                target: textButton1
                x: 440
                y: 550
                text: "Hauptmenü"
            }

            PropertyChanges {
                target: image1
                visible: false
            }
        },
        State {
            name: "unsuccessful_add"
            PropertyChanges {
                target: image
                x: 455
                y: 107
                source: "../images/error-905.svg"
            }

            PropertyChanges {
                target: text1
                text: qsTr("<b>Die Karte konnte aus unerklärlichen \n Gründen nicht hinzugefügt werden!</b>")
            }

            PropertyChanges {
                target: textButton
                visible: false
            }

            PropertyChanges {
                target: textButton1
                x: 440
                y: 550
                text: "Hauptmenü"
            }

            PropertyChanges {
                target: image1
                visible: false
            }
        },
        State {
            name: "already_exists"

            PropertyChanges {
                target: image
                x: 455
                y: 107
                source: "../images/error-905.svg"
            }

            PropertyChanges {
                target: text1
                y: 85
                width: 1445
                height: 157
                text: qsTr("Angelegte Karte existiert bereits in der Datenbank \n und kann nicht noch einmal hinzugefügt werden!")
                // \nLöschvorgang deshalb nicht möglich!")
            }

            PropertyChanges {
                target: textButton
                visible: false
            }

            PropertyChanges {
                target: textButton1
                x: 440
                y: 550
                text: "Hauptmenü"
            }

            PropertyChanges {
                target: image1
                visible: false
            }
        },
        State {
            name: "does_not_exists"

            PropertyChanges {
                target: text1
                y: 85
                width: 1445
                height: 157
                text: qsTr("<b>Angelegte Karte nicht in der Datenbank gefunden!</b>")
                // \nLöschvorgang deshalb nicht möglich!")
            }

            PropertyChanges {
                target: textButton
                visible: false
            }

            PropertyChanges {
                target: textButton1
                x: 440
                y: 550
                text: "Hauptmenü"
            }

            PropertyChanges {
                target: image1
                visible: false
            }
        },
        State {
            name: "delete_admin"
            PropertyChanges {
                target: image
                visible: true
                source: "../images/admin_fail.png"
            }

            PropertyChanges {
                target: text1
                text: qsTr("Karte des zu löschenden Administrators anlegen und scannen")
            }

            PropertyChanges {
                target: textButton
                y: 550
                text: "Scan"
            }

            PropertyChanges {
                target: textButton1
                y: 550
            }

            PropertyChanges {
                target: image1
                visible: false
            }
        },
        State {
            name: "delete_user"
            PropertyChanges {
                target: image
                source: "../images/user.png"
            }

            PropertyChanges {
                target: text1
                text: qsTr(
                          "Karte des zu löschenden Nutzers anlegen und scannen")
            }

            PropertyChanges {
                target: image1
                visible: false
            }
        },
        State {
            name: "authorize_new_admin"
            PropertyChanges {
                target: image
                visible: true
                source: "../images/admin.png"
            }

            PropertyChanges {
                target: text1
                text: qsTr("Karte des neuen Admin anlegen und scannen")
            }

            PropertyChanges {
                target: textButton
                y: 550
                text: "Scan"
            }

            PropertyChanges {
                target: textButton1
                y: 550
            }

            PropertyChanges {
                target: image1
                visible: false
            }
        },
        State {
            name: "successfully_deleted"

            PropertyChanges {
                target: image
                visible: true
                source: "../images/success.png"
            }

            PropertyChanges {
                target: text1
                text: qsTr("<b>Die Karte wurde erfolgreich \n aus der Datenbank gelöscht!</b>")
            }

            PropertyChanges {
                target: textButton
                visible: false
            }

            PropertyChanges {
                target: textButton1
                x: 440
                y: 550
                text: "Hauptmenü"
            }

            PropertyChanges {
                target: image1
                visible: false
            }
        },
        State {
            name: "unsuccessful_delete"

            PropertyChanges {
                target: image
                visible: true
                source: "../images/error-905.svg"
            }

            PropertyChanges {
                target: text1
                text: qsTr("<b>Die Karte konnte aus unerklärlichen \n Gründen nicht gelöscht werden!</b>")
                font.bold: false
            }

            PropertyChanges {
                target: textButton
                visible: false
            }

            PropertyChanges {
                target: textButton1
                x: 440
                y: 550
                text: "Hauptmenü"
            }

            PropertyChanges {
                target: image1
                visible: false
            }
        },
        State {
            name: "unsuccessful_delete_admin_via_all_users"

            PropertyChanges {
                target: image
                visible: true
                source: "../images/admin_fail.png"
            }

            PropertyChanges {
                target: text1
                text: qsTr("Löschvorgang fehlgeschlagen! Eine Admin Karte kann nur \n über den entsprechenden 'Admin löschen' Knopf geköscht werden!")
                font.bold: false
            }

            PropertyChanges {
                target: textButton
                visible: false
            }

            PropertyChanges {
                target: textButton1
                x: 440
                y: 550
                text: "Hauptmenü"
            }

            PropertyChanges {
                target: image1
                visible: false
            }
        }
    ]
}
