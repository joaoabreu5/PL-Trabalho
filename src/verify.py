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
    extraVar = None
    extraList = None
    for path in lst:
        level = 0
        node = tree
        for e in path:
            element = SingleInput(e,extraVar,extraList)
            if element not in node:
                node[element] = {}
                extraVar = None
                extraList = None
            else:
                if e["type"] == "any":
                    if extraVar is None:
                        extraVar = [(e["python"],level)]
                    else:
                        extraVar += [(e["python"],level)]
                elif e["type"] == "list_ht":
                    if extraList is None:
                        extraList = [(e["vars"],level)]
                    else:
                        extraList += [(e["vars"],level)]

            node = node[element]
            level+=1

    return tree


def verify_fill(list, tree):
    for element in list:
        path = element["input"]
        node = tree
        last = node
        aux = node
        for e in path:
            last = SingleInput(e)
            aux = node
            node = node[last]
        aux[last] = element["statement"]

    return tree


def str_tree(dict, level, length, varS):
    lenD = len(dict)
    j = 0
    if level == length:
        ret = dict + "\n"
    else:
        ret = ""
        for i in dict:
            extraVar = ""
            extraList = ""
            if i.extraVar != None:
                for e in i.extraVar:
                    extraVar += e[0]+ " = arg" + str(e[1])+"\n"
                varS = ""
            if i.extraList != None:
                for e in i.extraList:
                    index = 1
                    extraList += e[0][0] + " = arg" + str(e[1]) + "[0]\n"
                    while index < len(e[0]):
                        if index == len(e[0]) - 1:
                            extraList += e[0][index] + " = arg" + str(e[1]) + "[" + str(index) + ":]\n"
                        else:
                            extraList +=e[0][index] + " = arg" + str(e[1]) + "[" + str(index) + "]\n"
                        index += 1
                varS = ""

            if i.inputDict["type"] == 'any':
                ret+= extraVar
                ret+= extraList
                if level == length - 1:
                    ret += varS+i.inputDict["python"] + " = arg" + str(level) + "\n" + str_tree(dict[i], level + 1, length, "")
                else:
                    ret += str_tree(dict[i], level + 1, length,varS+i.inputDict["python"] + " = arg" + str(level)+ "\n")
            else:
                if j > 0:
                    ret += "el"
                if i.inputDict["type"] in ['num', 'boolean']:
                    if level == length - 1:
                        ret += "if arg" + str(level) + " == " + i.inputDict["python"] + ":\n\t" + re.sub(
                            '\n', '\n\t', varS+extraList+ extraVar+
                                                                                                        str_tree(dict[i],
                                                                                                                level + 1,
                                                                                                                length,""))
                    else:
                         ret += "if arg" + str(level) + " == " + i.inputDict["python"] + ":\n\t" + re.sub(
                            '\n', '\n\t', extraList + extraVar  +
                                                                                                        str_tree(dict[i],
                                                                                                                level + 1,
                                                                                                                length,varS))
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
                    
                    if level == length - 1:
                        ret += "if len(arg" + str(level) + ") >= " + str(len(i.inputDict["vars"]) - 1) + ":\n\t" + re.sub(
                            '\n', '\n\t', varS+ extraList + extraVar +aux+ str_tree(dict[i], level + 1, length,""))
                    else:
                        ret += "if len(arg" + str(level) + ") >= " + str(len(i.inputDict["vars"]) - 1) + ":\n\t" + re.sub(
                            '\n', '\n\t', extraList + extraVar + str_tree(dict[i], level + 1, length,varS+aux))
                        
                else:
                    if level == length - 1:
                        ret += "if len(arg" + str(level) + ") == 0" + ":\n\t" + re.sub(
                            '\n', '\n\t', varS + extraList + extraVar + str_tree(dict[i], level + 1, length,""))
                    else:
                        ret += "if len(arg" + str(level) + ") == 0" + ":\n\t"+ re.sub(
                            '\n', '\n\t', extraList + extraVar + str_tree(dict[i], level + 1, length,varS))
                if j == lenD - 1:
                    ret += "\nelse:\n\traise ValueError\n"
            if j != lenD - 1:
                ret += "\n"
            j += 1

    return ret
