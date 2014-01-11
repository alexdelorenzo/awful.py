import QtQuick 2.0

Rectangle {
    id: thread_qml

    width: 800
    height: 500
    
    ListView {
        id: thread_list

        width: parent.width
        height: parent.height

        AwfulThreadBar {
            id: thread_bar

            textsize: 12
            model: AwfulThreadModelObj
        }

        AwfulPosts {
            id: posts

            y: 25
            x:1

            width: parent.width - x - spacing
            height: thread_qml.height

            clip: true
            spacing: 5

            model: AwfulThreadModelObj
        }
    }
}
