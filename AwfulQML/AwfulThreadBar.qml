import QtQuick 2.0

Rectangle {

    id: thread_bar
    property var model: AwfulThreadModelObj
    property double textsize: 22

    width: parent.width
    height: thread_title.height 
    
    color: "#E8E8E8"

    Flow {
        id: thread_bar_flowbox

        Text {
            id: thread_title

            font.pointSize: thread_bar.textsize
            text: model.title
            color: "black"
            font.bold: true
            font.underline: true
        }

        AwfulPageSwitcher {
            id: switcher

            model: AwfulThreadModelObj
            textsize: thread_bar.textsize

            x: parent.width + switcher.width
        }
    }
}