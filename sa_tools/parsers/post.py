from sa_tools.parsers.parser import Parser
from sa_tools.base.sa_obj import SAObj

from bs4 import Tag


class PostParser(Parser):
    def __init__(self, *args, **kwargs):
        super(PostParser, self).__init__(*args, **kwargs)

    def parse(self, content: Tag=None) -> (str, tuple or str):
        if content is None:
            content = self.content

        super(PostParser, self).parse()
        yield 'user_info', parse_user_info(content=content)
        yield 'body', parse_post_body(content=content)


def parse_post_body(content: Tag) -> str:
    has_post = content.find('td', 'postbody')
    post = has_post.text.strip() if has_post else ""

    return post


def parse_user_info(content: Tag) -> (str, str, Tag):
    user_str = content.td['class'][-1].split('userid=')[-1]
    prefix = 'userid-'
    index = len(prefix)
    user_id = user_str[index:]
    user_name = content.dt.text
    info_content = content.find('td', 'userinfo')

    return user_id, user_name, info_content