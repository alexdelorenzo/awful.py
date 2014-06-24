import QtQuick 2.0
import QtQuick.Controls 1.0
import "Window.js" as WindowJS



ListView {
    id: threads_list

    clip: true

    width: parent.width
    height: parent.height

    model: AwfulIndexObj
    //highlight: Rectangle { color: "green"; radius: 5 }

    delegate: 
        Text {
            text: forum.title
            property var model: forum
            font.bold: true
            font.underline: true

            // MouseArea {
            //     anchors.fill: parent

            //     onClicked: {
            //         forum.read_page(1);
            //         var url = "WindowForum.qml";
            //         var winder = WindowJS.createWindow(forum, url);
            //     }
            // }
        }
    populate: Transition {
        NumberAnimation { properties: "x,y"; duration: 100 }
    }
    displaced: Transition {
        NumberAnimation { properties: "x,y"; duration: 10000 }
    }
}