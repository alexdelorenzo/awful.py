from SATools.SAParsers.SAParser import SAParser
from SATools.SATypes import IntOrNone


class SAForumParser(SAParser):
    def __init__(self, *args, **kwargs):
        super(SAForumParser, self).__init__(*args, **kwargs)

    def parse(self):
        super(SAForumParser, self).parse()

        if self.parent.is_index:
            return

        self.parse_subforums()
        self.parse_threads()

    def parse_subforums(self):
        if not self.has_subforums():
            return

        elif self.parent.children:
            self.parent._subforums_from_children()

        else:
            content = self.content
            tr_subforums = content.find_all('tr', 'subforum')

            for tr_subforum in tr_subforums:
                href = tr_subforum.a['href']
                subforum_id = href.split("forumid=")[-1]
                name = tr_subforum.a.text

                self.parent._add_subforum(subforum_id, name)

    def parse_threads(self):
        if self.unread:
            self.parse()

        self.content = self.content.find('div', id='content')
        thread_blocks = self.content.find_all('tr', 'thread', id=True)

        for tr_thread in thread_blocks:
            thread_id = IntOrNone.int_check(tr_thread['id'][6:])
            self.parent._add_thread(thread_id, tr_thread)

    def has_subforums(self):
        if self.children:
            return True

        content = self.content

        if content.table:
            return content.table['id'] == 'subforums'

        else:
            return False
