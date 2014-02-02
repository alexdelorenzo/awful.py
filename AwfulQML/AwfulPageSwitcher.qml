import QtQuick 2.0

Item {
    id: page_switcher

    property var model: AwfulThreadModelObj
    property double textsize: 12

    width: switcher_flowbox.width
    height: parent.height

    signal update()

    onUpdate: page_switcher.update_thread()

    function update_thread() {
         var int_page = parseInt(model.page)
         var int_pages = parseInt(model.pages)

         first_page.text = int_page <= 2 ? "" : "<<"
         prev_page.text = int_page <= 1 ? "" : "<"
         page_number.text = ''.concat(model.page, "/", model.pages)
         next_page.text = int_page >= int_pages ? "" : ">"
         last_page.text = int_page >= int_pages - 2 ? "" : ">>"

    }

    Component.onCompleted: page_switcher.update()

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