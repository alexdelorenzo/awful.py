import QtQuick 2.0

Rectangle {
    id: thread_qml

    width: 800
    height: 500
    
    ListView {
        id: thread_list
        spacing: 10
        width: parent.width
        height: parent.height

        AwfulThreadBar {
            id: thread_bar
            textsize: 12
            model: AwfulThreadModelObj
        }

        AwfulPosts {
            y: 25
            id: posts
            clip: true
            height: thread_qml.height

            model: AwfulThreadModelObj
        }
    }
}
