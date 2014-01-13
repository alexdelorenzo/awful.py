import QtQuick 2.0

Rectangle {
	id: post_box

	property double borderscale: 5

	width: parent.width
	height: parent.height * 0.14

	property double textsize: 12
	property var model: ''

	color: "#DFDFDF"

	Row {
		id: post_container

		width: parent.width
		height: parent.height
		x: borderscale
		anchors.verticalCenter: parent.verticalCenter

		spacing: borderscale

		PostTextBox {
			id: post_input

			y: borderscale
			height: parent.height - borderscale * 2
			width: parent.width - (borderscale * 3) - post_button.width
		}

		PostButton {
			id: post_button

			y: borderscale
			input_box: post_input
			height: parent.height - borderscale * 2
			model: post_box.model
		}
	}
}