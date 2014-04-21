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
        user_id = self.content.ul.a['href'].split('userid=')[-1]
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