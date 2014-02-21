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

	SplitView {
		//spacing: 5

		width: parent.width
		height: parent.height

		property variant model: parent.model

		Index {
			id: index

			model: main_window.model

			Layout.fillHeight: true

			onSelected: {
				var forum = Qt.createComponent("Forum.qml");
				var forum_obj = forum.createObject(tabs, {"model": item.model});
				forum_obj.model.read_page(1);
				//tabs.addTab(forum_obj.model.title, forum_obj);
			}
		}

		TabView {
		 	id: tabs

		 	Layout.fillHeight: true
		 	Layout.fillWidth: true

		 	tabsVisible: true
		 	frameVisible: false
		 }
	}
}