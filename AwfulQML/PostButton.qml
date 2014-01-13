import QtQuick 2.0 

Rectangle {
	id: post_button

	property var model: AwfulThreadModelObj
	property var input_box: ""

	width: post_button_label.width
	height: parent.height
	
	color: "#EEEEEE"

	Text {
		id: post_button_label

		text: "Post"
		color: "black"

		anchors.verticalCenter: parent.verticalCenter
	}
	
	MouseArea {
		anchors.fill: parent

		onClicked: {
			model.reply(input_box.text)
		}
	}
}