from bs4 import Tag

from sa_tools.parsers.parser import Parser


class InboxParser(Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, content: Tag) -> (iter, iter):
        content = super().parse(content)

        info_gen, pm_gen = gen_info(content), gen_pms(content)

        return info_gen, pm_gen


def gen_info(content):
    pass


def gen_pms(content):
    pm_table = content.find('table', 'standard')
    pms = pm_table.find_all('tr')

    yield from (pm for pm in pms if pm.td and not pm.option)
