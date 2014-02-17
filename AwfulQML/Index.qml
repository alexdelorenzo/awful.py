import QtQuick 2.0
import QtQuick.Window 2.1
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0


Rectangle {
	id: index_rect

	property variant model: AwfulIndexObj

	width: index_list.width
	height: parent.height

	color: "#ececec"

	ColumnLayout {
		spacing: 5

		width: parent.width
		height: parent.height

		property variant model: parent.model

		ScrollView {
			Layout.fillHeight: true
			
			IndexList {
				id: index_list

				model: index_rect.model
				spacing: 1
			}
		}
	}
}