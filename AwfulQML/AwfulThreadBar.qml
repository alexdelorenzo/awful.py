import QtQuick 2.0

Rectangle {
    id: thread_bar

    property var model: ''
    property double textsize: 8

    signal toggled(bool yesno)

    onToggled: console.log("blip")

    width: parent.width
    height: thread_title.height 

    color: "#E8E8E8"

    Flow {
        id: thread_bar_flowbox
        spacing: 10

        width: parent.width
        height: parent.height

        Text {
            id: thread_title

            font.pointSize: thread_bar.textsize
            text: thread_bar.model.title
            color: "black"
            font.bold: true
            font.underline: true

            MouseArea {
                id: title_mouse
                anchors.fill: parent

                onClicked: {
                    thread_bar.toggled(true)
                }
            }
        }

        AwfulPageSwitcher {
            id: switcher

            model: thread_bar.model
            textsize: thread_bar.textsize
        }
    }
}