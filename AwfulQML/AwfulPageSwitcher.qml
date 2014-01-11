import QtQuick 2.0

Rectangle {
    id: page_switcher

    property var model: AwfulThreadModelObj
    property double textsize: 12
    anchors.right: parent.right

    function update_thread()
    {
         page_number.text = ''.concat(model.page, " of ", model.pages)
    }

    Text {
        id: left_arrow

        font.pointSize: page_switcher.textsize
        text: "<"

        MouseArea {
            anchors.fill: parent
            onClicked: {
                model.prev_page();
                page_switcher.update_thread()}
            }
        }

    Text {
        id: page_number

        anchors.left: left_arrow.right
        font.pointSize: page_switcher.textsize
        text: parent.update_thread()
    }

    Text{
        id: right_arrow

        anchors.left: page_number.right
        font.pointSize: page_switcher.textsize
        text: ">"

        MouseArea {
            anchors.fill: parent
            onClicked: {model.next_page()
                page_switcher.update_thread()}
        }
    }
}