import QtQuick 2.0
import QtQuick.Controls 1.0

Button {
	id: post_button

	property var model: AwfulThreadModelObj
	property var input_box: ""

	width: text.width
	height: text.height
	
	//color: "#EEEEEE"

	text: "Post"

	onClicked: {
        console.log(model.id)
        console.log(input_box.getText())
        model.reply(input_box.getText())
    }
}
