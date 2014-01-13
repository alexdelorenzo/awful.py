import QtQuick 2.0

Item {
    id: page_switcher

    property var model: AwfulThreadModelObj
    property double textsize: 12

    width: switcher_flowbox.width
    height: parent.height
    

    function update_thread() {
         page_number.text = ''.concat(model.page, "/", model.pages)
    }

    Flow {
        id: switcher_flowbox
        spacing: 5

        Text {
            id: first_page

            font.pointSize: page_switcher.textsize
            text: "<<"

            MouseArea {
                anchors.fill: parent

                onClicked: {
                    model.first_page()
                    page_switcher.update_thread()
                }
            }
        }

        
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

        TextInput {
            id: page_number

            //anchors.left: prev_page.right
            font.pointSize: page_switcher.textsize
            text: page_switcher.update_thread()

            MouseArea {
                anchors.fill: parent

                onClicked: {
                    model.read_page(model.page)
                    page_switcher.update_thread()
               }
            }
        }

        Text {
            id: next_page

            //anchors.left: page_number.right
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

        Text {
            id: last_page

            font.pointSize: page_switcher.textsize
            text: ">>"

            MouseArea {
                anchors.fill: parent

                onClicked: {
                    model.last_page();
                    page_switcher.update_thread()
                }
            }
        }
    }
}