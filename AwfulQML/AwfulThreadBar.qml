import QtQuick 2.0

Rectangle {
    id: thread_bar

    property var model: ''
    property double textsize: 8

    signal toggled(bool yesno)

    onToggled: {
        thread_title.apply_lr_changes();
    }

    Component.onCompleted: {
        thread_title.apply_lr_changes();
    }

    width: parent.width
    height: thread_title.height 

    color: "#E8E8E8"

    Flow {
        id: thread_bar_flowbox
        spacing: 10

        width: parent.width - last_read.width
        height: parent.height

        Text {
            id: thread_title

            text: thread_bar.model.title

            font.bold: true
            font.underline: true
            font.pointSize: thread_bar.textsize
            color: "black"

            elide: Text.ElideRight

            function apply_lr_changes () {
                var has_lr = thread_bar.model.has_lr;

                if (has_lr) {
                    var unread_posts = parseInt(thread_bar.model.last_read.unread_count);

                    if (unread_posts > 0){
                        thread_title.font.bold = true;
                        thread_title.font.italic = false;
                        thread_title.text = "[*] " + thread_bar.model.title;
                        }
                    else {
                        thread_title.font.bold = false;
                        thread_title.font.italic = true;
                        thread_title.text = thread_bar.model.title;
                    }

                }
            }

            MouseArea {
                id: title_mouse
                anchors.fill: parent

                onClicked: {
                    thread_bar.toggled(true)
                }
            }
        }

        AwfulPageSwitcher {
            id: switcher

            model: thread_bar.model
            textsize: thread_bar.textsize
        }
    }

    LastRead {
        id: last_read

        model: thread_bar.model
        update_this: switcher
        color: 'orange' //thread_bar.color

        visible: is_visible()

        function toggle_visibility() {
            var is_visible = last_read.is_visible();

            if (is_visible){
                last_read.visible = last_read.visible ? false : true;}
        }

        function is_visible () {
            var has_lr = thread_bar.model.has_lr ?  true : false;
            var is_overlapping = (thread_bar.width - thread_bar_flowbox.width <= 0);

            return (!is_overlapping && has_lr);
        }

        x: parent.width - width
    }
}