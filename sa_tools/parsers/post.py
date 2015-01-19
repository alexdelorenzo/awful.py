from sa_tools.parsers.parser import Parser
from sa_tools.base.sa_obj import SAObj

from sa_tools.parsers.tools.wrapper import BeauToLxml, BS4Adapter


class PostParser(Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, content: BS4Adapter) -> (str, tuple or str):
        content = self.wrap(content, wrapper=BeauToLxml)
        yield 'user_info', parse_user_info(content=content)
        yield 'body', parse_post_body(content=content)


def parse_post_body(content: BS4Adapter) -> str:
    has_post = content.find('td', 'postbody')
    post = has_post.text.strip() if has_post else ""

    return post


def parse_user_info(content: BS4Adapter) -> (str, str, BS4Adapter):
    user_id = content.td['class'][-1].split('userid-')[-1]
    user_name = content.dt.text
    info_content = content.find('td', 'userinfo')

    return user_id, user_name, info_content