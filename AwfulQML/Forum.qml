import QtQuick 2.0


Rectangle {
	id: forum_rect

	property var model: AwfulForumModelObj
	
	width: parent.width
	height: parent.height

	color: "#c1c1c1"

	Column {
		spacing: 5

		width: parent.width
		height: parent.height

		AwfulThreadBar {
			id: thread_bar

			model: forum_rect.model
			textsize: 10
		}

		ThreadsList {
			id: thread_list

			model: forum_rect.model
			spacing: 1
		}
	}
}