import QtQuick 2.0

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

        Text {
            id: username

            width: post_frame.width

            color:'black'
            font.pointSize: 11
            verticalAlignment: Text.AlignTop
            
            text: post.poster
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

    }
}
