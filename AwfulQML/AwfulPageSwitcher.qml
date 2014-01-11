import QtQuick 2.0

Rectangle {
    id: page_switcher

    property var model: AwfulThreadModelObj
    property double textsize: 12
    
    anchors.right: parent.right

    function update_thread() {
         page_number.text = ''.concat(model.page, " of ", model.pages)
    }

    Flow {
        id: switcher_flowbox
        
        Text {
            id: prev_page

            font.pointSize: page_switcher.textsize
            text: "<"

            MouseArea {
                anchors.fill: parent

                onClicked: {
                    model.prev_page();
                    page_switcher.update_thread()
                }
            }
        }

        Text {
            id: page_number

            anchors.left: prev_page.right
            font.pointSize: page_switcher.textsize
            text: page_switcher.update_thread()
        }

        Text {
            id: next_page

            anchors.left: page_number.right
            font.pointSize: page_switcher.textsize
            text: ">"

            MouseArea {
                anchors.fill: parent

                onClicked: {
                    model.next_page()
                    page_switcher.update_thread()
                }
            }
        }
    }
}