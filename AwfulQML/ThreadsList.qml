import QtQuick 2.0 
import QtQuick.Window 2.1

ListView {
    id: threads_list
    
    width: parent.width
    height: parent.height

    clip: true

    model: AwfulForumModelObj

    delegate:
        AwfulThread {
            model: thread
        }
        
    populate: Transition {
        NumberAnimation { properties: "x,y"; duration: 300 }
    }
    displaced: Transition {
        NumberAnimation { properties: "x,y"; duration: 1000 }
    }
}