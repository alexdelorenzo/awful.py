import QtQuick 2.0

Rectangle {
    id: thread_qml

    width: 800
    height: 500

    color: thread_bar.color
    
    Column {
        id: thread_list

        width: parent.width
        height: parent.height

        anchors.fill: parent
        spacing: 5

        AwfulThreadBar {
            id: thread_bar

            textsize: 11
            model: AwfulThreadModelObj
        }

        AwfulPosts {
            id: posts
            x: spacing

            width: thread_qml.width - x - spacing
            height: thread_qml.height - post_box.height - 16 - spacing*2

            clip: true
            spacing: 5

            model: AwfulThreadModelObj
        }

        PostBox {
            id: post_box
            model: AwfulThreadModelObj
        }
    }
}
