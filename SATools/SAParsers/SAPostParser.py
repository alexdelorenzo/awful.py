from SATools.SAParsers.SAParser import SAParser


class SAPostParser(SAParser):
    def __init__(self, *args, **kwargs):
        super(SAPostParser, self).__init__(*args, **kwargs)

    def parse(self):
        super(SAPostParser, self).parse()
        self._parse_from_thread()

    def _parse_from_thread(self):
        self._parse_user_info()
        self._parse_post_body()

    def _parse_user_info(self):
        user_str = self.content.td['class'][-1].split('userid=')[-1]
        prefix = 'userid-'
        index = len(prefix)

        user_id = user_str[index:]
        user_name = self.content.dt.text
        info_content = self.content.find('td', 'userinfo')

        self.parent._add_poster(user_id, user_name, info_content)

    def _parse_post_body(self):
        has_post = self.content.find('td', 'postbody')

        if has_post:
            post = has_post.text.strip()

        else:
            post = ""

        self.parent.body = post