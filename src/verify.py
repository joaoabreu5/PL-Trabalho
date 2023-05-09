from singleInput import SingleInput
import re


def verify_UNARY_BOOL_OP(t):
    r = None
    if t == 'any' or t == 'boolean':
        r = 'boolean'
    return r


def verify_UNARY_NUM_OP(t):
    r = None
    if t == 'any' or t == 'num':
        r = 'num'
    return r


def verify_BIN_NUM_OP(t1, t2):
    r = None
    if (t1 == 'any' or t1 == 'num') and (t2 == 'any' or t2 == 'num'):
        r = 'num'
    return r


def verify_BIN_BOOL_OP(t1, t2):
    r = None
    if (t1 == 'any' or t1 == 'boolean') and (t2 == 'any' or t2 == 'boolean'):
        r = 'boolean'
    return r


def verify_BIN_COMPARE_OP(t1, t2):
    r = verify_EQUALTYPE(t1, t2)

    if r is not None:
        r = 'boolean'
    return r


def verify_LIST(t):
    r = None
    if t.startswith('list_') or t == 'any':
        r = t
    return r


def verify_COLON(t1, t2):
    r = None
    t1_list_count = t1.count('list_')
    t2_list_count = t2.count('list_')

    if t1 == 'any':
        if t2 == 'any':
            r = 'any'
        elif t2_list_count > 0:
            r = t2
    elif t2 == 'any':
        if t1 == 'any':
            r = 'any'
        else:
            r = 'list_' + t1
    elif t2_list_count == t1_list_count + 1:
        t1_list_type = t1[t1_list_count * 5:]
        t2_list_type = t2[t2_list_count * 5:]

        if t1_list_type == t2_list_type:
            r = t2
        elif t2_list_type == '':
            r = 'list_' + t1

    return r


def verify_CONCAT(t1, t2):
    r = None
    t1_list_count = t1.count('list_')
    t2_list_count = t2.count('list_')

    if t1 == 'any':
        if t2 == 'any':
            r = 'any'
        elif t2_list_count > 0:
            r = t2
    elif t2 == 'any':
        if t1 == 'any':
            r = 'any'
        elif t1_list_count > 0:
            r = t1
    elif t2_list_count == t1_list_count:
        r = verify_EQUALTYPE(t1, t2)

    return r


def verify_EQUALTYPE(t1, t2):
    r = None
    t1_list_count = t1.count('list_')
    t2_list_count = t2.count('list_')

    if t1 == 'any':
        r = t2
    elif t2 == 'any':
        r = t1
    elif t1_list_count == t2_list_count:
        t1_list_type = t1[t1_list_count * 5:]
        t2_list_type = t2[t2_list_count * 5:]
        if t1_list_type == t2_list_type:
            r = t1
        elif t1_list_type == '':
            r = t2
        elif t2_list_type == '':
            r = t1
    return r


def verify_ERROR(t, line, col, expected, actual, expression):
    if t is None:
        raise Exception(
            f"{line}:{col}: <type error> Couldn't match expected type '{expected}' with actual type '{actual}, in expression '{expression}'")


def verify_group_by_level(lst):
    tree = {}
    for path in lst:
        node = tree
        for e in path:
            element = SingleInput(e)
            if element not in node:
                node[element] = {}
            node = node[element]

    return tree


def verify_fill(list, tree):
    for element in list:
        path = element["input"]
        node = tree
        laste = node
        aux = node
        for e in path:
            laste = SingleInput(e)
            aux = node
            node = node[laste]
        aux[laste] = element["statement"]

    return tree


def str_tree(dict, level, length):
    lenD = len(dict)
    j = 0
    if level == length:
        ret = dict + "\n"
    else:
        ret = ""
        for i in dict:
            if i.inputDict["type"] == 'any':
                ret += i.inputDict["python"] + " = arg" + str(level) + "\n" + str_tree(dict[i], level + 1, length)
            else:
                if j > 0:
                    ret += "el"
                if i.inputDict["type"] in ['num', 'boolean']:
                    ret += "if arg" + str(level) + " == " + i.inputDict["python"] + ":\n\t" + re.sub('\n', '\n\t',
                                                                                                     str_tree(dict[i],
                                                                                                              level + 1,
                                                                                                              length))
                elif i.inputDict["type"] == "list_ht":
                    aux = ""
                    index = 1
                    aux += i.inputDict["vars"][0] + " = arg" + str(level) + "[0]\n"
                    while index < len(i.inputDict["vars"]):
                        if index == len(i.inputDict["vars"]) - 1:
                            aux += i.inputDict["vars"][index] + " = arg" + str(level) + "[" + str(index) + ":]\n"
                        else:
                            aux += i.inputDict["vars"][index] + " = arg" + str(level) + "[" + str(index) + "]\n"
                        index += 1

                    ret += "if len(arg" + str(level) + ") >= " + str(len(i.inputDict["vars"]) - 1) + ":\n\t" + re.sub(
                        '\n', '\n\t', aux) + re.sub('\n', '\n\t', str_tree(dict[i], level + 1, length))
                else:
                    ret += "if len(arg" + str(level) + ") == 0" + ":\n\t" + re.sub('\n', '\n\t',
                                                                                   str_tree(dict[i], level + 1, length))
                if j == lenD - 1:
                    ret += "\nelse:\n\traise ValueError\n"
            if j != lenD - 1:
                ret += "\n"
            j += 1

    return ret
