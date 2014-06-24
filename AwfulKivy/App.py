import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from awful import AwfulPy

class AwfulKivyApp(App):
    def build(self):
        awful_py = AwfulPy('salisbury shake', '7?Dasqsaluf6')
        index = IndexWidget(awful_py)
        return index


class IndexWidget(Widget):
    def __init__(self, ap):
        super(IndexWidget, self).__init__()
        self.ap = ap
        self.forums = []

    def setup_forums(self):
        forums = self.ap.index.forums.values()
        self.forums = list(map(ForumWidget, forums))


class ForumWidget(Widget):
    def __init__(self, sa_forum):
        super(ForumWidget, self).__init__()
        self.forum = sa_forum
        self.title = sa_forum

if __name__== "__main__":
    AwfulKivyApp().run()