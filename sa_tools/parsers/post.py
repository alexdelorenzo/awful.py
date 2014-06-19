from sa_tools.parsers.parser import SAParser
from sa_tools.base.sa_obj import SAObj


class SAPostParser(SAParser):
    def __init__(self, *args, **kwargs):
        super(SAPostParser, self).__init__(*args, **kwargs)
        self.user_info = None
        self.body = None

    def parse(self):
        super(SAPostParser, self).parse()
        self.user_info = self.parse_user_info(content=self.content)
        self.body = self.parse_post_body(content=self.content)

    @staticmethod
    def parse_user_info(content):
        user_str = content.td['class'][-1].split('userid=')[-1]
        prefix = 'userid-'
        index = len(prefix)
        user_id = user_str[index:]
        user_name = content.dt.text
        info_content = content.find('td', 'userinfo')

        return user_id, user_name, info_content

    @staticmethod
    def parse_post_body(content):
        has_post = content.find('td', 'postbody')
        post = has_post.text.strip() if has_post else ""

        return post

class PostAdapter(SAObj):
    pass