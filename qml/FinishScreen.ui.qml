import QtQuick 2.15

ScreenCommon {
    id: root
    height: Constants.height
    width: Constants.width
    caption.y: 30

    signal clicked
    signal cancel
    signal retry

    property var cuLaterTexts: [qsTr("Bis später!"), qsTr(
            "Genießen Sie Ihren Aufenthalt an der DHBW!"), qsTr(
            "Bis Spätersilie!"), qsTr("Bis speda, Peda!"), qsTr(
            "Bis Baldrian!"), qsTr("Bis Dannzig!"), qsTr(
            "Man siebt sich!"), qsTr("Bis Dennis!"), qsTr(
            "Bis denn, Sven!"), qsTr("Bis denn, Sven!")]
    property var byeByeTexts: [qsTr("Bis zum nächsten Mal!"), qsTr(
            "Bitte beehren Sie uns bald wieder!"), qsTr(
            "Bitte kommen Sie bald wieder!"), qsTr(
            "Wir hoffen der Akku ist voll geworden!"), qsTr(
            "Wir wünschen eine angenehme Radfahrt!"), qsTr(
            "San Frantschüssko!"), qsTr("Tschüsseldorf!"), qsTr(
            "Tschö mit ö!"), qsTr("Tschau mit au!"), qsTr(
            "Tschüsli Müsli!"), qsTr("Sayonara Carbonara!"), qsTr(
            "Ciao Kakao!")]

    Image {
        id: image
        x: 289
        y: 172
        width: 600
    }

    Text {
        id: bottomText
        text: "BOTTOM TEXT"
        anchors.bottom: parent.bottom
        font.pixelSize: 64
        horizontalAlignment: Text.AlignHCenter
        anchors.bottomMargin: 30
        anchors.horizontalCenter: parent.horizontalCenter
        font.family: Constants.fontFamily

        Connections {
            target: bottomText
            function onVisibleChanged() {
                if (visible) {
                    let texts = state === "deposit" ? cuLaterTexts : byeByeTexts
                    bottomText.text = texts[Math.floor(Math.random(
                                                           ) * texts.length)]
                }
            }
        }
    }

    MouseArea {
        id: mouseArea
        width: parent.width
        height: parent.height

        Connections {
            target: mouseArea
            function onClicked(){
                root.clicked()
            } 
        }
    }

    Image {
        id: image1
        x: 539
        y: 350
        width: 100
        height: 100
        visible: false
        source: "qrc:/qtquickplugin/images/template_image.png"
        fillMode: Image.PreserveAspectFit
    }

    TextButton {
        id: textButton
        x: 24
        y: 664
        visible: false

        Connections {
            target: textButton
            function onClicked(mouse) {
                root.retry()
            }
        }
    }

    TextButton {
        id: textButton1
        x: 14
        y: 672
        visible: false

        Connections {
            target: textButton1
            function onClicked(mouse) {
                root.cancel()
            }
        }
    }

    states: [
        State {
            name: "deposit"

            PropertyChanges {
                target: root
                caption.text: qsTr("Bitte Akku anstecken und Türe schließen!")
            }

            PropertyChanges {
                target: image
                source: "../images/AkkuEinlegen.png"
            }

            PropertyChanges {
                target: image1
                visible: false
            }

            PropertyChanges {
                target: textButton
                x: 37
                y: 664
                visible: false
            }

            PropertyChanges {
                target: textButton1
                x: 27
                y: 672
                visible: false
            }

            PropertyChanges {
                target: mouseArea
                x: 0
                y: 0
            }
        },
        State {
            name: "retrieve"

            PropertyChanges {
                target: root
                caption.text: qsTr("Bitte Akku entnehmen und Türe schließen!")
            }

            PropertyChanges {
                target: image
                source: "../images/AkkuEntnehmen.png"
            }

            PropertyChanges {
                target: image1
                visible: false
            }

            PropertyChanges {
                target: textButton1
                x: 31
                y: 672
                visible: false
            }

            PropertyChanges {
                target: textButton
                x: 872
                y: 672
                visible: false
            }
        },
        State {
            name: "permission_denied"

            PropertyChanges {
                target: image1
                x: 256
                y: 165
                width: 768
                height: 470
                visible: true
                source: "../images/permission_denied.png"
            }

            PropertyChanges {
                target: root
                caption.text: qsTr(
                                  "Mit dieser Karte kommst du hier nicht rein!")
            }

            PropertyChanges {
                target: textButton
                x: 77
                y: 651
                visible: true
                text: "Erneut  scannen"
            }

            PropertyChanges {
                target: textButton1
                x: 804
                y: 641
                visible: true
                text: "Abbruch"
            }

            PropertyChanges {
                target: bottomText
                visible: false
            }
        }
    ]
}



