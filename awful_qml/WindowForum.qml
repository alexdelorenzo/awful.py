import QtQuick 2.0
import QtQuick.Window 2.1
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0

Window {
	id: forum_window

	property variant model: parent.model

	title: model.title

	width: 550
	height: 500

	color: "#ececec"

	ColumnLayout {
		spacing: 5

		width: parent.width
		height: parent.height

		property variant model: parent.model

		Forum {
			Layout.fillWidth: true
			Layout.fillHeight: true

			id: forum_qml

			model: forum_window.model

			state: 'read'
		}
	}
}