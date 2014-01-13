import QtQuick 2.0

Rectangle {
	id: stretchy_edge

	property var horizontal: false
	property var vertical: false

	width: 0
	height: 0

	function change_parent () {
		if (horizontal)
			parent.width = x
		else
			parent.y = y
	}

	Flickable {
		id: stretchy_grip

		width: parent.width
		height: parent.height

		anchors.fill: parent

		onFlickEnded: {
			if (stretchy_grip.movingHorizontally)
				if (!stretchy_edge.horizontal)
					stretchy_grip.cancleFlick()
			else if (!stretchy_edge.vertical)
				stretchy_grip.cancleFlick()
		}
	}

}