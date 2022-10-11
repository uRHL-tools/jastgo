import json

__CURRENT_ALPHA = ["!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4",
                   "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H",
                   "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\",
                   "]", "^", "_", "`", " "]
__DICT_SIZE = len(__CURRENT_ALPHA)
__CURRENT_DICT = {}

base_dir = '/home/redwing/PycharmProjects/ptil-stegotool/db'
file = 'java_lang_String.json'


def parse_java_class(json_file):
    """

    :param json_file: JSON file containing the class information (fields, constructors and parameters)
    :return: The java class mapped into a dictionary
    """
    # json_file = open(f'{base_dir}/{file}')
    json_file = open(f'{json_file}')
    java_class = json.load(json_file)
    json_file.close()
    return java_class


def count_total_elems(json_file):
    jc = parse_java_class(json_file)
    count = 0
    for attr in jc:
        count += len(jc[attr])
    return count


def elem_type_count(json_file, javaclass_attr):
    """

    :param json_file:
    :param javaclass_attr: Should be one of: 'fields', 'constructors',  'methods'
    :return:
    """
    jc = parse_java_class(json_file)
    return len(jc[javaclass_attr])


def to_string(json_file):
    jc = parse_java_class(json_file)
    for attr, values in jc.items():
        if attr == 'fields':
            print(f'')
            # TODO: parse java class fields
        elif attr == 'constructors':
            print(f'')
            for val in values:
                print(f'{val}')
        elif attr == 'methods':
            print(f'')
            for val in values:
                print(f'{val["returnType"]} {val["nameAndParams"]}')
        else:
            print(f'[WARN] JavaClassMapper.to_string(): Unrecognized java class attribute "{attr}"')

    print(f'{"-" * 55}')
    for k in jc:
        print(f'{k} elem. count\t{elem_type_count(json_file, k)}')

    print(f'{"-" * 55}\nTOTAL elem. count\t\t{count_total_elems(json_file)}')


def method_attr_to_string(elem):
    return f'{elem["returnType"]} {elem["nameAndParams"]}'


def map_to_dict(javaclass_json):
    jc_dict = {}
    jc = parse_java_class(f'{javaclass_json}')
    for i in range(0, __DICT_SIZE):
        jc_dict.update({__CURRENT_ALPHA[i]: method_attr_to_string(jc['methods'][i])})
    return jc_dict

