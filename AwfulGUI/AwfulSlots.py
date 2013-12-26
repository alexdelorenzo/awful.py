__author__ = 'alex'
from AwfulGUI.AwfulForum import AwfulThreadList
from AwfulGUI.AwfulThread import AwfulThread, AwfulThreadDocker
from PyQt5.QtCore import Qt

class AwfulSlots(object):
	def __init__(self, application_obj):
		self.forums = SlotsForumsList(application_obj)
		self.threads = SlotsThreadsList(application_obj)


class SlotsForumsList(object):
	def __init__(self, application_obj):
		self.app = application_obj
		self.forums_list = self.app.vbox_lists.list_forums
		self.threads_list = self.app.vbox_lists.list_threads
		self.layout = self.app.vbox_lists.layout

		self.setup_slots_signals()


	def setup_slots_signals(self):
		self.forums_list.itemActivated.connect(self.signal_item_activated)

	def signal_item_activated(self, list_item=None):
		forum = list_item.forum

		self.threads_list.hide()
		self.threads_list = AwfulThreadList(forum)
		self.layout.addWidget(self.threads_list)

class SlotsThreadsList(SlotsForumsList):
	def __init__(self, application_obj):
		super().__init__(application_obj)
		self.gridbox = self.app.vbox_console.grid_threads
		self.layout = self.gridbox.layout

	def setup_slots_signals(self):
		self.threads_list.itemActivated.connect(self.signal_item_activated)

	def signal_item_activated(self, list_item=None):
		thread = list_item.thread

		self.gridbox.addDockWidget(Qt.DockWidgetArea(1), AwfulThreadDocker(thread))






def main():
	pass


if __name__ == "__main__":
	main()