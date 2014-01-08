import QtQuick 2.0

ListView {
    id: thread_list
    width: 800
    height: 500
    spacing: 5

    snapMode: ListView.SnapToItem
    model: AwfulThreadModelObj


    delegate: AwfulPost {
        poster: post.poster
        body: post.body
    }

    populate: Transition {
        NumberAnimation { properties: "x,y"; duration: 1000 }
    }

    AwfulThreadBar {
        model: model
    }


}
