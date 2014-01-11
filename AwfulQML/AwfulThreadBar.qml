import QtQuick 2.0

Rectangle {

    id: thread_bar
    property var model: AwfulThreadModelObj
    property double textsize: 22

    width: parent.width
    anchors.fill: parent
    color: "#AAA"

    Flow{
        Text {
            id: thread_title

            font.pointSize: thread_bar.textsize
            text: model.title
            color: "black"
            font.bold: true
            font.underline: true
            elide: Text.ElideLeft
        }

        AwfulPageSwitcher {
            id: switcher

            model: AwfulThreadModelObj
            textsize: thread_bar.textsize

            x: parent.width + switcher.width

            }

    }
}