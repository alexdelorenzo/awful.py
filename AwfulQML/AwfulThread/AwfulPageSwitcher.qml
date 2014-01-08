import QtQuick 2.0

Item {
   // x: parent.width - width

    property var model: AwfulThreadModelObj
    id: thread_bar
    anchors.right: parent.right

    Text {
        font.pointSize: 12
        id: left_arrow
        text: "<"
        MouseArea {
            anchors.fill: parent
            onClicked: {
                AwfulThreadModelObj.prev_page();
                page_number.text = AwfulThreadModelObj.page}
            }
        }

    Text {
        anchors.left: left_arrow.right
        font.pointSize: 12
        id: page_number
        text: AwfulThreadModelObj.page

    }

    Text{
        anchors.left: page_number.right
        font.pointSize: 12
        id: right_arrow
        text: ">"
        MouseArea {
            anchors.fill: parent
            onClicked: {AwfulThreadModelObj.next_page()
                page_number.text = AwfulThreadModelObj.page}
        }
    }
}