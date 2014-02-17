import QtQuick 2.0
import QtQuick.Layouts 1.0
import QtQuick.Controls 1.0


Rectangle {
    id: post_frame

    property string poster: ''
    property string body: ''

    width: parent.width
    height: username.height + post_text.height

    color: "#F4F4F4"

    
    Rectangle {
        id: username_box

        width: parent.width
        height: username.height
        color: "#EEEEEE"

        RowLayout {
            Text {
                id: username

                color:'black'
                font.pointSize: 11
                
                text: post.poster

                Layout.alignment: Qt.AlignLeft
                Layout.rowSpan: 0
            }
            CheckBox {
                id: chk_box

                text: "Quote"
                Layout.alignment: Qt.AlignRight
                Layout.fillWidth: true

                visible: false

                onClicked: {}
            }
        }   
    }

    Text {
        id: post_text

        y: username.height
        width: parent.width
        anchors.topMargin: y

        textFormat: Text.RichText
        wrapMode: Text.Wrap

        text: post.content

        onLinkActivated: Qt.openUrlExternally(link)

    }

    MouseArea {
        id: username_ma

        width: parent.width
        height: parent.height
        
        hoverEnabled: true

        onEntered: chk_box.visible = true
        onExited: chk_box.visible = chk_box.checked ? true : false
        onClicked: chk_box.checked = chk_box.checked ? false : true
    }

}
