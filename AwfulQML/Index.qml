import QtQuick 2.0
import QtQuick.Window 2.1
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0


Rectangle {
	id: index_rect

	signal selected(Item item)

	property variant model: AwfulIndexObj

	width: 190
	height: parent.height

	color: "#f4f4f4"

	RowLayout {
		spacing: 5

		width: parent.width
		height: parent.height

		property variant model: parent.model

		IndexList {
			id: index_list
			Layout.fillHeight: true
			model: index_rect.model
			spacing: 1

			MouseArea {
				id: _mouse

				anchors.fill: parent

				onClicked: {
					var item = index_list.itemAt(mouse.x, mouse.y);
					index_rect.selected(item);
				}
			}
		}
	}
}