import QtQuick 2.0


Rectangle {
	id: forum_rect

	property variant model: AwfulForumModelObj
	
	width: parent.width
	height: parent.height

	color: "#ececec"

	Column {
		spacing: 5

		width: parent.width
		height: parent.height

		property variant model: parent.model

		AwfulThreadBar {
			id: thread_bar

			model: parent.model
			textsize: 10
		}

		ThreadsList {
			id: thread_list

			model: forum_rect.model
			spacing: 1
		}
	}
}