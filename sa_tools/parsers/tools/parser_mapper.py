from os import listdir

sa_prefix = 'SA'
prefix_index = len(sa_prefix)

sa_tools = listdir('..')
sa_parsers = listdir('../parsers')



def index_of(file_name, find_str='.'):
    if find_str in file_name:
        return file_name.index(find_str)

    else:
        return None


def prefix(file_name, prefix_str='SA'):
    if prefix_str is not None:
        prefix_index = len(prefix_str)

    else:
        return 0

    return file_name[:prefix_index]


def suffix(file_name, suffix_str=None):
    if suffix_str is not None:
        index = index_of(file_name, suffix_str)

    else:
        index = index_of(file_name)

    if index is None:
        return len(file_name)

    else:
        return file_name[index:]


def noun(file_name, prefix_str='SA', suffix_str='Parser'):
    prefix_index = index_of(file_name, prefix_str)
    suffix_index = index_of(file_name, suffix_str)

    return file_name[prefix_index:suffix_index]


#
# def noun(file_name):
#     if suffix(file_name):
#         suffix_index = index_of(file_name)
#         file_name = file_name[prefix_index:suffix_index]
#
#     parser_str = 'Parser'
#     if parser_str in file_name:
#         parser_index = index_of(file_name, parser_str)
#         file_name = file_name[:parser_index]
#
#     return file_name


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


def get_names(file_list):
    names = sorted(gen_sa_modules(file_list))
    return names


def get_name_map(names):
    nouns = module_nouns(names)
    name_map = dict(zip(nouns, names))
    return name_map


def get_parser_map():
    module_names = get_names(sa_tools)
    parser_names = get_names(sa_parsers)

    sa_modules_map = get_name_map(module_names)
    sa_parser_map = get_name_map(parser_names)

    parser_map = dict()

    for module_noun in sa_modules_map:
        if module_noun in sa_parser_map:
            parser_noun = sa_modules_map[module_noun]
            module_noun = 'SA' + module_noun

        else:
            continue

        parser_map[module_noun] = parser_noun

    return parser_map


def import_statement(parser_name):
    package = "from sa_tools.parsers." + parser_name
    import_cmd = "import " + parser_name

    statement = package + ' ' + import_cmd

    return statement


def get_import_statement_map(parser_map=None):
    if not parser_map:
        parser_map = get_parser_map()

    import_map = {module_noun: import_statement(parser_name)
                  for module_noun, parser_name in parser_map.items()}

    return import_map

