import QtQuick 2.0

Item {

    id: thread_bar
    property var model: AwfulThreadModelObj



    AwfulPageSwitcher {
        model: model
        }

}