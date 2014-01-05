__author__ = 'alex'
from AwfulGUI_old.AwfulForum import AwfulThreadList
from AwfulGUI_old.AwfulThread import AwfulThread, AwfulThreadDocker
from PyQt5.QtCore import Qt


class AwfulSlots(object):
	def __init__(self, application_obj):
		self.forums = SlotsForumsList(application_obj)
		self.threads = SlotsThreadsList(application_obj)


class SlotsForumsList(object):
	def __init__(self, application_obj):
		self.app = application_obj
		self.setup_slots_signals()

	def setup_slots_signals(self):
		self.app.vbox_lists.list_forums.itemActivated.connect(self.signal_item_activated)

	def signal_item_activated(self, list_item):
		list_item.forum.read()
		forum = list_item.forum

		if not forum.threads:
			forum.read()

		self.app.vbox_lists.list_threads.close()

		self.app.vbox_lists.list_threads = \
			AwfulThreadList(forum)

		self.app.vbox_lists.setup_sizes()
		self.app.slots.threads.setup_slots_signals()


class SlotsThreadsList(SlotsForumsList):
	def __init__(self, application_obj):
		super().__init__(application_obj)
		self.gridbox = self.app.vbox_console.grid_threads
		self.layout = self.gridbox.layout
		self.dock_area = 6

	def setup_slots_signals(self):
		self.app.vbox_lists.list_threads.itemActivated.connect(self.signal_item_activated)

	def signal_item_activated(self, list_item=None):
		thread = list_item.thread

		if not thread.posts:
			thread.read()

		self.gridbox.addDockWidget(Qt.DockWidgetArea(self.dock_area % 5), AwfulThreadDocker(thread))
		self.dock_area += 1
		self.setup_slots_signals()


def main():
	pass


if __name__ == "__main__":
	main()