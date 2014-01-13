import QtQuick 2.0

ListView {
    id: posts_list
    
    width: parent.width
    height: parent.height

    model: AwfulThreadModelObj
    delegate: AwfulPost {
        poster: post.poster
        body: post.body
    }

    populate: Transition {
        NumberAnimation { properties: "x,y"; duration: 250 }
    }
}
