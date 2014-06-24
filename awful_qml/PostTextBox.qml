import QtQuick 2.0
import QtQuick.Controls 1.0

Rectangle {
	id: post_input

	height: parent.height
	width: parent.width

	color: "#F4F4F4"

	function getText() {
		return post_input_box.getText(0, post_input_box.length)
	}
	
	TextArea {
		id: post_input_box

		height: parent.height
		width: parent.width

		//backgroundVisible: false
	}
}
