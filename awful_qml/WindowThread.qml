import QtQuick 2.0
import QtQuick.Window 2.1
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0

Window {
	id: thread_window

	property variant model: parent.model

	title: model.title

	width: 500
	height: thread_qml.height

	color: "#ececec"

	ColumnLayout {
		spacing: 5

		width: parent.width
		height: parent.height

		property variant model: parent.model

		AwfulThread {
			Layout.fillWidth: true
			Layout.fillHeight: true
			id: thread_qml

			model: thread_window.model

			state: 'read'
		}
	}
}