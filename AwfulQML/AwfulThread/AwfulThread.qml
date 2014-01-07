import QtQuick 2.0

ListView {
    id: thread_list
    width: 300
    height: 500
    model: AwfulThreadModelObj

    delegate: AwfulPost {
        poster: post.poster
        body: post.body
    }
}