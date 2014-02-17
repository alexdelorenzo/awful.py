import QtQuick 2.0
import QtQuick.Window 2.1
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0


ApplicationWindow {
	id: main_window

	property variant model: AwfulIndexObj

	width: parent.width
	height: parent.height

	title: 'AwfulPy 0.0.1'

	color: "#ececec"

	ColumnLayout {
		spacing: 5

		width: parent.width
		height: parent.height

		property variant model: parent.model

		Index {
			id: index

			model: main_window.model

			Layout.fillHeight: true
		}

		// TabView {
		// 	id: tab_view

		// 	Layout.fillHeight: true
		// 	visible: false
		// }
	}
}