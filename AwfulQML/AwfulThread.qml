import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0
import QtQuick.Window 2.1
import "Window.js" as WindowJS

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
    
    ColumnLayout {
        id: thread_list
        
        spacing: 1

        AwfulThreadBar {
            id: thread_bar

            textsize: 8
            model: thread_qml.model

            Layout.minimumWidth: thread_qml.width
            Layout.maximumWidth: thread_qml.width

            onToggled: {
                model.read_page(model.page)
                if (thread_qml.state == 'list') {
                    var url = "WindowThread.qml";
                    var winder = WindowJS.createWindow(model, url);
                    }
                else {
                    //thread_qml.state = 'list'
                }
            }
        }
        SplitView {
            Layout.maximumHeight: thread_qml.height - thread_bar.height
            Layout.minimumHeight: thread_qml.height

            Layout.minimumWidth: thread_qml.width
            Layout.maximumWidth: thread_qml.width 
            orientation: Qt.Vertical


            AwfulPosts {
                id: posts

                x: spacing
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
                height: 500 
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
