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

		if not forum.threads:
			forum.read()

		self.threads_list.clear()
		self.threads_list.__init__(forum)

class SlotsThreadsList(SlotsForumsList):
	def __init__(self, application_obj):
		super().__init__(application_obj)
		self.gridbox = self.app.vbox_console.grid_threads
		self.layout = self.gridbox.layout
		self.dock_area = 6

	def setup_slots_signals(self):
		self.threads_list.itemActivated.connect(self.signal_item_activated)
		print('rawhide')

	def signal_item_activated(self, list_item=None):
		thread = list_item.thread
		print(thread)

		if not thread.posts:
			thread.read()

		self.gridbox.addDockWidget(Qt.DockWidgetArea(self.dock_area % 5), AwfulThreadDocker(thread))
		self.dock_area += 1
		self.setup_slots_signals()






def main():
	pass


if __name__ == "__main__":
	main()