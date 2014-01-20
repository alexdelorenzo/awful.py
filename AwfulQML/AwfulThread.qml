import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0

Rectangle {
    id: thread_qml

    property var model: AwfulThreadModelObj
    property int page: 0
    property int spacing: 0

    width: parent.width
    height: parent.height

    color: thread_bar.color
    state: 'list'

    Component.onCompleted: {
        if (0 < page)
            model.read_page(page)
    }   
    
    Column {
        id: thread_list

        width: parent.width
        height: parent.height

        anchors.fill: parent
        spacing: 5

        AwfulThreadBar {
            id: thread_bar

            textsize: 8
            model: thread_qml.model

            Layout.maximumHeight: height
            Layout.minimumHeight: height

            onToggled: {
                if (thread_qml.state == 'list') {
                    thread_qml.state = 'read'
                    model.read_page(model.page)
                    //console.log('list -> read')
                    }
                else {
                    thread_qml.state = 'list'
                    //console.log('read - > list')
                }
            }
        }
        SplitView {
                height: parent.height - thread_bar.height
                width: parent.width
                orientation: Qt.Vertical

            AwfulPosts {
                id: posts

                x: spacing
                width: thread_qml.width - spacing*2
                height: thread_qml.height - post_box.height - spacing*2 - 16

                clip: true
                spacing: 5

                model: thread_qml.model

                Layout.fillHeight: true
            }

            PostBox {
                id: post_box
                model: thread_qml.model
            }
        }
       }

    states: [
        State {
            name: 'list'

            PropertyChanges {
                target: thread_qml
                height: thread_bar.height
            }
            PropertyChanges {
                target: posts
                visible: false
            }
            PropertyChanges {
                target: post_box
                visible: false
            }
        },

        State {
            name: 'read'
            PropertyChanges {
                target: thread_qml
                height: 300
            }

            PropertyChanges {
                target: posts
                visible: true
            }
            PropertyChanges {
                target: post_box
                visible: true
            }
        }

    ]

    transitions: [
            Transition {
            id: toggled_trans
            from: 'list'
            to: 'read'

            reversible: true
            enabled: true
            NumberAnimation { properties: "height,width"; duration: 125 }
        }
    ]
}
