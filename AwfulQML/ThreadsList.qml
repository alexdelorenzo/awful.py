import QtQuick 2.0 

ListView {
    id: threads_list
    
    width: parent.width
    height: parent.height

    clip: true

    model: AwfulForumModelObj

    delegate: AwfulThread {
        model: thread
    }

    populate: Transition {
        NumberAnimation { properties: "x,y"; duration: 250 }
    }
}