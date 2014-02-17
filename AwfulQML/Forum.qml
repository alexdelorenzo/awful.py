import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0

import "Window.js" as WindowJS

Rectangle {
	id: forum_rect

	property variant model: AwfulForumModelObj
	
	width: parent.width
	height: parent.height

	color: "#ececec"
    state: 'read'

	Component.onCompleted: console.log('blip')

	Column {
		spacing: 5

		width: parent.width
		height: parent.height

		property variant model: parent.model

		AwfulThreadBar {
			id: thread_bar

			model: parent.model
			textsize: 10

			onToggled: {
                model.read_page(model.page);
                if (forum_rect.state == 'list') {
                    var url = "WindowForum.qml";
                    var winder = WindowJS.createWindow(model, url);
                }
                else {
                    forum_rect.state = 'list'
                }
            }
		}

		ThreadsList {
			id: thread_list

			model: forum_rect.model
			spacing: 1
		}
	}

	 states: [
        State {
            name: 'list'

            PropertyChanges {
                target: forum_rect
                height: thread_bar.height
            }
            
            PropertyChanges {
                target: thread_list
                visible: false
            }
        },

        State {
            name: 'read'

            PropertyChanges {
                target: forum_rect
                height: parent.height
            }

            PropertyChanges {
                target: thread_list
                visible: true
            }
        }
    ]
}