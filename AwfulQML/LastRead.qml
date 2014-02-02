import QtQuick 2.0

Rectangle {
    id: last_read

    property variant model: AwfulThreadModelObj
    property variant update_this: ""

    width: lr_flow.width * 1.2
    height: parent.height

    border.color: "#BAB9B7"
    border.width: 1

    gradient: Gradient {
        GradientStop { position: 0.0; color: "#ececec"}
        GradientStop { position: 1.0; color: "orange" }
    }

    Row {
        id: lr_flow

        width: unread_count.width + stop_tracking.width + 2
        height: parent.height

        spacing: 5

        Text {
            id: stop_tracking
            text: "X"

            MouseArea {
                anchors.fill: parent

                 onClicked: {
                    last_read.model.last_read.stop()
                 }
            }

        }
        Text {
            id: unread_count
            text: last_read.model.has_lr ?  last_read.model.last_read.unread_count : ""

            MouseArea {
                anchors.fill: parent

                 onClicked: {
                    last_read.model.last_read.jump();
                    last_read.update_this.update()
                 }
            }
        }
    }
}