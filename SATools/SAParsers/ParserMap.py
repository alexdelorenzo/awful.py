from os import listdir


prefix_index = len('SA')


def index_of(file_name, find_str='.'):
    if find_str in file_name:
        return file_name.index(find_str)

    else:
        return None


def prefix(file_name, prefix_str='SA'):
    if prefix_str is not None:
        prefix_index = len(prefix_str)

    return file_name[:prefix_index]


def suffix(file_name, suffix_str=None):
    if suffix_str is not None:
        index = index_of(file_name, suffix_str)

    else:
        index = index_of(file_name)

    return file_name[index:]


def noun(file_name):
    if suffix(file_name):
        suffix_index = index_of(file_name)
        file_name = file_name[prefix_index:suffix_index]

    parser_str = 'Parser'
    if parser_str in file_name:
        parser_index = index_of(file_name, parser_str)
        file_name = file_name[:parser_index]

    return file_name


def is_py(file_name):
    return suffix(file_name) == '.py'


def is_sa(file_name):
    return prefix(file_name) == 'SA'


def is_sa_module(file_name):
    return is_py(file_name) and is_sa(file_name)


def gen_sa_modules(file_list):
    modules_gen = (file_name for file_name in file_list
                   if is_sa_module(file_name))

    return modules_gen


def gen_nouns(file_list):
    modules_gen = gen_sa_modules(file_list)
    nouns_gen = map(noun, modules_gen)

    return nouns_gen


def module_nouns(file_list):
    nouns = sorted(gen_nouns(file_list))

    return nouns


def first_occurrence(item, sequence):
    if item in sequence:
        return item

    return False


sa_tools = listdir('..')
sa_parsers = listdir('../SAParsers')

module_names = sorted(gen_sa_modules(sa_tools))
parser_names = sorted(gen_sa_modules(sa_parsers))

sa_module_nouns = module_nouns(module_names)
sa_parser_nouns = module_nouns(parser_names)

sa_modules_map = dict(zip(sa_module_nouns, module_names))
sa_parser_map = dict(zip(sa_parser_nouns, parser_names))

#