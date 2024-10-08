import ply.yacc as yacc
import lexer
import verify
import re
from caseInput import CaseInput

tokens = lexer.tokens

start = 'fpy_program'


def substitute_func_name(match, functions):
    word = match.group(1)
    fm = match.group(0)
    if word in functions:
        return "f_" + word + "_"+"("
    return fm


def p_fpy_program(p):
    """
    fpy_program : FPYINIT function_declarations FPYCLOSE
                | FPYINIT FPYCLOSE
    """
    if len(p) == 3:
        p[0] = ""
    else:
        for func in p[2]["func_called"]:
            if func[2] not in p.parser.functions:
                inputText = p.lexer.lexdata
                line = func[0]
                col = lexer.find_column(inputText, lexpos=func[1])
                raise Exception(f"{line}:{col}: <scope error> Function '{func[2]}' not in scope")
            
        code = ""
        for func in sorted(p.parser.newFunctions, key=lambda x: (p.parser.functions[x]["lineno"], p.parser.functions[x]["col"])):
            code += p.parser.functions[func]["python"]

        pattern = r'(\b\w+\b)\s*\('
        finalCode = re.sub(pattern, lambda match: substitute_func_name(match, p.parser.functions), code)
        p[0] = finalCode


def p_function_declarations(p):
    """ 
    function_declarations : function_declaration
                          | function_declaration function_declarations
    """
    p[0] = {}
    if len(p) == 2:
        p[0]["func_called"] = p[1]["func_called"]
    else:
        p[0]["func_called"] = p[1]["func_called"] + p[2]["func_called"]
    func_name = p[1]["func_name"]
    line = p[1]["lineno"]
    col = lexer.find_column(p.lexer.lexdata, lexpos=p[1]["lexpos"])
    if func_name in p.parser.functions:
        if line < p.parser.functions[func_name]["lineno"]:
            oldline = p.parser.functions[func_name]["lineno"]
            oldcol = p.parser.functions[func_name]["col"]
            p.parser.warnings.append((oldline, oldcol, f"{oldline}:{oldcol}: <Warning> Function '{func_name}' is already defined"))
            p.parser.functions[func_name] = {"lineno": line, "col": col, "python": p[1]["python"]}
        elif line == p.parser.functions[func_name]["lineno"]:
            if col < p.parser.functions[func_name]["col"]:
                oldline = p.parser.functions[func_name]["lineno"]
                oldcol = p.parser.functions[func_name]["col"]
                p.parser.warnings.append((oldline, oldcol, f"{oldline}:{oldcol}: <Warning> Function '{func_name}' is already defined"))
                p.parser.functions[func_name] = {"lineno": line, "col": col, "python": p[1]["python"]}
            else:
                p.parser.warnings.append((line, col, f"{line}:{col}: <Warning> Function '{func_name}' is already defined"))
        else:
            p.parser.warnings.append((line, col, f"{line}:{col}: <Warning> Function '{func_name}' is already defined"))
    else:
        p.parser.functions[func_name] = {"lineno": line, "col": col, "python": p[1]["python"]}
        p.parser.newFunctions += [func_name]


def p_function_declaration(p):
    """ 
    function_declaration : DEFF IDENTIFIER LBRACE function_body RBRACE
    """
    line = p.lineno(1)
    col = lexer.find_column(p.lexer.lexdata, lexpos=p.lexpos(1))
    setLen = set()
    setInput = set()
    toBeRemoved = []
    for l in p[4]:
        lineL = l["lineno"]
        colL = lexer.find_column(p.lexer.lexdata, lexpos=l["lexpos"])
        setLen.add(len(l["input"]))
        entry = CaseInput(l["input"])
        if entry in setInput:
            toBeRemoved.append(l)
            p.parser.warnings.append((lineL, colL, f"{lineL}:{colL}: <Warning> Redundant input in pattern matching for function '{p[2]}'")),
        else:
            setInput.add(entry)

    for l in toBeRemoved:
        p[4].remove(l)

    if len(setLen) > 1:
        raise Exception(f"{line}:{col}: <Error> Equations for function '{p[2]}' have different number of arguments")

    lenArgs = setLen.pop()
    if lenArgs > 0:
        sortedIn = sorted(list(setInput), reverse=True)
        lista = map(lambda x: x.inputCase, sortedIn)
        listaL = list(lista)
        tree = verify.verify_group_by_level(listaL)
        tree = verify.verify_fill(p[4], tree)
        pythonString = verify.str_tree(tree, 0, lenArgs, "")
    else:
        pythonString = p[4][0]["statement"]

    func_declare_string = "def " + p[2] + "("
    for i in range(lenArgs):
        if i != lenArgs - 1:
            func_declare_string += "arg" + str(i) + ", "
        else:
            func_declare_string += "arg" + str(i)
    func_declare_string += "):"
    full_function = func_declare_string + "\n\t" + re.sub("\n", "\n\t", pythonString) + "\n\n"
    p[0] = {}
    p[0]["func_name"] = p[2]
    p[0]["python"] = full_function
    p[0]["lineno"] = p.lineno(1)
    p[0]["lexpos"] = p.lexpos(1)
    p[0]["func_called"] = [item for d in p[4] for item in d["func_called"]]


def p_function_body(p):
    """ 
    function_body : case_statement SEMICOLON
                  | case_statement SEMICOLON function_body
    """
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_case_statement(p):
    """ 
    case_statement : CASE case_input ASSIGN statement
    """
    varsUsed = p[4]["vars"]
    for var in sorted(varsUsed, key=lambda x: x[1]):
        varsInfo = [item for d in p[2] for item in d["infoVars"]]
        varsIn = [t[-1] for t in varsInfo]
        if var[2] not in varsIn:
            inputText = p.lexer.lexdata
            line = var[0]
            col = lexer.find_column(inputText, lexpos=var[1])
            raise Exception(f"{line}:{col}: <scope error> Variable '{var[2]}' not in scope")
        
    p[0] = {}
    p[0]["statement"] = p[4]["python"]
    p[0]["input"] = p[2]
    p[0]["lineno"] = p.lineno(1)
    p[0]["lexpos"] = p.lexpos(1)
    p[0]["func_called"] = p[4]["func_called"]


def p_case_input(p):
    """ 
    case_input : LPAREN RPAREN
               | LPAREN case_arguments RPAREN
    """
    if len(p) == 3:
        p[0] = []
    else:
        p[0] = p[2]


def p_case_arguments(p):
    """ 
    case_arguments : case_argument
                   | case_argument COMMA case_arguments
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        varsInfo = [item for d in p[3] for item in d["infoVars"]]
        varsIn = [t[-1] for t in varsInfo]
        for v in p[1]["infoVars"]:
            if v[2] in varsIn:
                for tup in sorted(varsInfo, key=lambda x: x[1]):
                    if tup[2] == v[2]:
                        result = tup
                        break
                inputText = p.lexer.lexdata
                line = result[0]
                col = lexer.find_column(inputText, lexpos=result[1])
                raise Exception(f"{line}:{col}: <scope error> Variable '{result[2]}' already in scope")
        p[0] = [p[1]] + p[3]
        

def p_case_argument(p):
    """ 
    case_argument : constant
                  | case_list
    """
    p[0] = p[1]


def p_constant(p):
    """ 
    constant : flo
             | int
             | bool
             | id
    """
    p[0] = p[1]
    p[0]["infoVars"] = p[1]["vars"]


def p_case_list(p):
    """
    case_list : case_empty
              | case_headtail
    """
    p[0] = p[1]


def p_case_empty(p):
    """ 
    case_empty : LSQUARE RSQUARE 
    """
    p[0] = {}
    p[0]["type"] = "list_empty"
    p[0]["vars"] = []
    p[0]["infoVars"] = []
    p[0]["lineno"] = p.lineno(1)
    p[0]["lexpos"] = p.lexpos(1)
    p[0]["lastpos"] = p.lexpos(2)


def p_case_headtail(p):
    """ 
    case_headtail : IDENTIFIER COLON case_headtail2 
    """
    varsIn = [t[-1] for t in p[3]["infoVars"]]
    if p[1] in varsIn:
        for tup in sorted(p[3]["infoVars"], key=lambda x: x[1]):
            if tup[2] == p[1]:
                result = tup
                break
        inputText = p.lexer.lexdata
        line = result[0]
        col = lexer.find_column(inputText, lexpos=result[1])
        raise Exception(f"{line}:{col}: <scope error> Variable '{result[2]}' already in scope")
        
    p[0] = {}
    p[0]["type"] = "list_ht"
    p[0]["vars"] = [p[1]] + p[3]["vars"]
    p[0]["infoVars"] = [(p.lineno(1), p.lexpos(1), p[1])] + p[3]["infoVars"]


def p_case_headtail2(p):
    """ 
    case_headtail2 : case_headtailID
                   | case_headtail
    """
    p[0] = p[1]


def p_case_headtailID(p):
    """
    case_headtailID : IDENTIFIER
    """
    p[0] = {}
    p[0]["vars"] = [p[1]]
    p[0]["infoVars"] = [(p.lineno(1), p.lexpos(1), p[1])]


def p_statement(p):
    """ 
    statement : IF expr THEN statement ELSE statement
              | expr
    """
    if len(p) == 2:
        p[0] = p[1]
        p[0]["python"] = "return " + p[1]["python"]
    else:
        t = verify.verify_UNARY_BOOL_OP(p[2]["type"])
        verify.verify_ERROR(t, p.lineno(1) + p.lineno(2), lexer.find_column(p.lexer.lexdata, lexpos=p[2]["lexpos"]),
                            "boolean", p[2]["type"], p.lexer.lexdata[p[2]["lexpos"]:p[2]["lastpos"]])
        t = verify.verify_EQUALTYPE(p[4]["type"], p[6]["type"])
        verify.verify_ERROR(t, p.lineno(1) + p.lineno(6), lexer.find_column(p.lexer.lexdata, lexpos=p[6]["lexpos"]),
                            p[4]["type"], p[6]["type"], p.lexer.lexdata[p[6]["lexpos"]:p[6]["lastpos"]])

        p[0] = {}
        p[0]["type"] = t
        p[0]["python"] = "if " + re.sub("return ", "", p[2]["python"]) + ":\n\t" + re.sub(r'\n', '\n\t', p[4][
            "python"]) + "\nelse:\n\t" + re.sub(r'\n', '\n\t', p[6]["python"])
        p[0]["lexpos"] = p.lexpos(1)
        p[0]["lineno"] = p.lineno(1)
        p[0]["lastpos"] = p[6]["lastpos"]
        p[0]["vars"] = p[2]["vars"] + p[4]["vars"] + p[6]["vars"]
        p[0]["func_called"] = p[2]["func_called"]+p[4]["func_called"]+p[6]["func_called"]


def p_list(p):
    """
    list : LSQUARE RSQUARE
         | LSQUARE list_elements RSQUARE
    """
    if len(p) == 3:
        p[0] = {}
        p[0]["type"] = "list_"
        p[0]["python"] = "[]"
        p[0]["lastpos"] = p.lexpos(2) + 1
        p[0]["func_called"] = []
        p[0]["vars"] = []
    else:
        p[0] = {}
        p[0]["type"] = "list_" if p[2]["type"] == "any" else "list_" + p[2]["type"]
        p[0]["python"] = "[" + p[2]["python"] + "]"
        p[0]["lastpos"] = p.lexpos(3) + 1
        p[0]["func_called"] = p[2]["func_called"]
        p[0]["vars"] = p[2]["vars"]
    p[0]["lexpos"] = p.lexpos(1)
    p[0]["lineno"] = p.lineno(1)


def p_list_elements(p):
    """ 
    list_elements : expr
                  | expr COMMA list_elements
    """

    if len(p) == 2:
        p[0] = p[1]
    else:
        t = verify.verify_EQUALTYPE(p[1]["type"], p[3]["type"])
        verify.verify_ERROR(t, p[1]["lineno"], lexer.find_column(p.lexer.lexdata, lexpos=p[1]["lexpos"]), p[3]["type"],
                            p[1]["type"], p.lexer.lexdata[p[1]["lexpos"]:p[1]["lastpos"]])

        p[0] = {}
        p[0]["type"] = t
        p[0]["python"] = p[1]["python"] + ", " + p[3]["python"]
        p[0]["lexpos"] = p[1]["lexpos"]
        p[0]["lineno"] = p[1]["lineno"]
        p[0]["vars"] = p[1]["vars"] + p[3]["vars"]
        p[0]["func_called"] = p[1]["func_called"]+p[3]["func_called"]
        

def p_expr(p):
    """ 
    expr : expr OR join 
         | join
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        t = verify.verify_UNARY_BOOL_OP(p[1]["type"])
        verify.verify_ERROR(t, p[1]["lineno"], lexer.find_column(p.lexer.lexdata, lexpos=p[1]["lexpos"]), "boolean",
                            p[1]["type"], p.lexer.lexdata[p[1]["lexpos"]:p[1]["lastpos"]])
        t = verify.verify_UNARY_BOOL_OP(p[3]["type"])
        verify.verify_ERROR(t, p[3]["lineno"], lexer.find_column(p.lexer.lexdata, lexpos=p[3]["lexpos"]), "boolean",
                            p[3]["type"], p.lexer.lexdata[p[3]["lexpos"]:p[3]["lastpos"]])

        p[0] = {}
        p[0]["type"] = t
        p[0]["python"] = p[1]["python"] + " or " + p[3]["python"]
        p[0]["lexpos"] = p[1]["lexpos"]
        p[0]["lineno"] = p[1]["lineno"]
        p[0]["lastpos"] = p[3]["lastpos"]
        p[0]["vars"] = p[1]["vars"] + p[3]["vars"]
        p[0]["func_called"] = p[1]["func_called"]+p[3]["func_called"]


def p_join(p):
    """ 
    join : join AND equality
         | equality
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        t = verify.verify_UNARY_BOOL_OP(p[1]["type"])
        verify.verify_ERROR(t, p[1]["lineno"], lexer.find_column(p.lexer.lexdata, lexpos=p[1]["lexpos"]), "boolean",
                            p[1]["type"], p.lexer.lexdata[p[1]["lexpos"]:p[1]["lastpos"]])
        t = verify.verify_UNARY_BOOL_OP(p[3]["type"])
        verify.verify_ERROR(t, p[3]["lineno"], lexer.find_column(p.lexer.lexdata, lexpos=p[3]["lexpos"]), "boolean",
                            p[3]["type"], p.lexer.lexdata[p[3]["lexpos"]:p[3]["lastpos"]])

        p[0] = {}
        p[0]["type"] = t
        p[0]["python"] = p[1]["python"] + " and " + p[3]["python"]
        p[0]["lexpos"] = p[1]["lexpos"]
        p[0]["lineno"] = p[1]["lineno"]
        p[0]["lastpos"] = p[3]["lastpos"]
        p[0]["vars"] = p[1]["vars"] + p[3]["vars"]
        p[0]["func_called"] = p[1]["func_called"]+p[3]["func_called"]


def p_equality(p):
    """ 
    equality : equality EQ rel 
             | equality NE rel
             | rel
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        t = verify.verify_BIN_COMPARE_OP(p[1]["type"], p[3]["type"])
        verify.verify_ERROR(t, p[3]["lineno"], lexer.find_column(p.lexer.lexdata, lexpos=p[3]["lexpos"]), p[1]["type"],
                            p[3]["type"], p.lexer.lexdata[p[3]["lexpos"]: p[3]["lastpos"]])

        p[0] = {}
        p[0]["type"] = t
        p[0]["python"] = p[1]["python"] + " " + p[2] + " " + p[3]["python"]
        p[0]["lexpos"] = p[1]["lexpos"]
        p[0]["lineno"] = p[1]["lineno"]
        p[0]["lastpos"] = p[3]["lastpos"]
        p[0]["vars"] = p[1]["vars"] + p[3]["vars"]
        p[0]["func_called"] = p[1]["func_called"]+p[3]["func_called"]


def p_rel(p):
    """
    rel : listop LT listop 
        | listop GT listop
        | listop LE listop
        | listop GE listop
        | listop
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        t = verify.verify_BIN_COMPARE_OP(p[1]["type"], p[3]["type"])
        verify.verify_ERROR(t, p[3]["lineno"], lexer.find_column(p.lexer.lexdata, lexpos=p[3]["lexpos"]), p[1]["type"],
                            p[3]["type"], p.lexer.lexdata[p[3]["lexpos"]: p[3]["lastpos"]])
        p[0] = {}
        p[0]["type"] = t
        p[0]["python"] = p[1]["python"] + " " + p[2] + " " + p[3]["python"]
        p[0]["lexpos"] = p[1]["lexpos"]
        p[0]["lineno"] = p[1]["lineno"]
        p[0]["lastpos"] = p[3]["lastpos"]
        p[0]["vars"] = p[1]["vars"] + p[3]["vars"]
        p[0]["func_called"] = p[1]["func_called"]+p[3]["func_called"]


def p_listop(p):
    """
    listop : sum COLON listop
           | sum CONCAT listop
           | sum
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {}
        if p[2] == ':':
            t = verify.verify_LIST(p[3]["type"])
            verify.verify_ERROR(t, p[3]["lineno"], lexer.find_column(p.lexer.lexdata, lexpos=p[3]["lexpos"]), "list",
                                p[3]["type"], p.lexer.lexdata[p[3]["lexpos"]:p[3]["lastpos"]])
            t = verify.verify_COLON(p[1]["type"], p[3]["type"])
            verify.verify_ERROR(t, p[3]["lineno"], lexer.find_column(p.lexer.lexdata, lexpos=p[3]["lexpos"]),
                                "list_" + p[1]["type"], p[3]["type"], p.lexer.lexdata[p[3]["lexpos"]:p[3]["lastpos"]])
            p[0]["python"] = "[" + p[1]["python"] + "]" + " + " + p[3]["python"]
        else:
            t = verify.verify_LIST(p[1]["type"])
            verify.verify_ERROR(t, p[1]["lineno"], lexer.find_column(p.lexer.lexdata, lexpos=p[1]["lexpos"]), "list",
                                p[1]["type"], p.lexer.lexdata[p[1]["lexpos"]:p[1]["lastpos"]])
            t = verify.verify_LIST(p[3]["type"])
            verify.verify_ERROR(t, p[3]["lineno"], lexer.find_column(p.lexer.lexdata, lexpos=p[3]["lexpos"]), "list",
                                p[3]["type"], p.lexer.lexdata[p[3]["lexpos"]:p[3]["lastpos"]])
            t = verify.verify_CONCAT(p[1]["type"], p[3]["type"])
            verify.verify_ERROR(t, p[3]["lineno"], lexer.find_column(p.lexer.lexdata, lexpos=p[3]["lexpos"]),
                                p[1]["type"], p[3]["type"], p.lexer.lexdata[p[3]["lexpos"]:p[3]["lastpos"]])
            p[0]["python"] = p[1]["python"] + " + " + p[3]["python"]

        p[0]["type"] = t
        p[0]["lexpos"] = p[1]["lexpos"]
        p[0]["lineno"] = p[1]["lineno"]
        p[0]["lastpos"] = p[3]["lastpos"]
        p[0]["vars"] = p[1]["vars"] + p[3]["vars"]
        p[0]["func_called"] = p[1]["func_called"]+p[3]["func_called"]


def p_sum(p):
    """ 
    sum : sum PLUS term
         | sum MINUS term
         | term
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        t = verify.verify_UNARY_NUM_OP(p[1]["type"])
        verify.verify_ERROR(t, p[1]["lineno"], lexer.find_column(p.lexer.lexdata, lexpos=p[1]["lexpos"]), "num",
                            p[1]["type"], p.lexer.lexdata[p[1]["lexpos"]:p[1]["lastpos"]])
        t = verify.verify_UNARY_NUM_OP(p[3]["type"])
        verify.verify_ERROR(t, p[3]["lineno"], lexer.find_column(p.lexer.lexdata, lexpos=p[3]["lexpos"]), "num",
                            p[3]["type"], p.lexer.lexdata[p[3]["lexpos"]:p[3]["lastpos"]])

        p[0] = {}
        p[0]["type"] = t
        p[0]["python"] = p[1]["python"] + " " + p[2] + " " + p[3]["python"]
        p[0]["lexpos"] = p[1]["lexpos"]
        p[0]["lineno"] = p[1]["lineno"]
        p[0]["lastpos"] = p[3]["lastpos"]
        p[0]["vars"] = p[1]["vars"] + p[3]["vars"]
        p[0]["func_called"] = p[1]["func_called"]+p[3]["func_called"]


def p_term(p):
    """ 
    term : term MULT exponential
         | term DIV exponential
         | term FLOORDIV exponential 
         | term MOD exponential
         | exponential
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        t = verify.verify_UNARY_NUM_OP(p[1]["type"])
        verify.verify_ERROR(t, p[1]["lineno"], lexer.find_column(p.lexer.lexdata, lexpos=p[1]["lexpos"]), "num",
                            p[1]["type"], p.lexer.lexdata[p[1]["lexpos"]:p[1]["lastpos"]])
        t = verify.verify_UNARY_NUM_OP(p[3]["type"])
        verify.verify_ERROR(t, p[3]["lineno"], lexer.find_column(p.lexer.lexdata, lexpos=p[3]["lexpos"]), "num",
                            p[3]["type"], p.lexer.lexdata[p[3]["lexpos"]:p[3]["lastpos"]])

        p[0] = {}
        p[0]["type"] = t
        p[0]["python"] = p[1]["python"] + " " + p[2] + " " + p[3]["python"]
        p[0]["lexpos"] = p[1]["lexpos"]
        p[0]["lineno"] = p[1]["lineno"]
        p[0]["lastpos"] = p[3]["lastpos"]
        p[0]["vars"] = p[1]["vars"] + p[3]["vars"]
        p[0]["func_called"] = p[1]["func_called"]+p[3]["func_called"]


def p_exponential(p):
    """ 
    exponential : exponential POWER unary
                | unary
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        t = verify.verify_UNARY_NUM_OP(p[1]["type"])
        verify.verify_ERROR(t, p[1]["lineno"], lexer.find_column(p.lexer.lexdata, lexpos=p[1]["lexpos"]), "num",
                            p[1]["type"], p.lexer.lexdata[p[1]["lexpos"]:p[1]["lastpos"]])
        t = verify.verify_UNARY_NUM_OP(p[3]["type"])
        verify.verify_ERROR(t, p[3]["lineno"], lexer.find_column(p.lexer.lexdata, lexpos=p[3]["lexpos"]), "num",
                            p[3]["type"], p.lexer.lexdata[p[3]["lexpos"]:p[3]["lastpos"]])

        p[0] = {}
        p[0]["type"] = t
        p[0]["python"] = p[1]["python"] + " " + p[2] + " " + p[3]["python"]
        p[0]["lexpos"] = p[1]["lexpos"]
        p[0]["lineno"] = p[1]["lineno"]
        p[0]["lastpos"] = p[3]["lastpos"]
        p[0]["vars"] = p[1]["vars"] + p[3]["vars"]
        p[0]["func_called"] = p[1]["func_called"]+p[3]["func_called"]


def p_unary(p):
    """ 
    unary : NOT unary 
          | MINUS unary 
          | PLUS unary
          | factor
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[1] == '!':
            t = verify.verify_UNARY_BOOL_OP(p[2]["type"])
            p[1] = 'not'
            verify.verify_ERROR(t, p[2]["lineno"], lexer.find_column(p.lexer.lexdata, lexpos=p[2]["lexpos"]), "boolean",
                                p[2]["type"], p.lexer.lexdata[p.lexpos(1):p[2]["lastpos"]])
        else:
            t = verify.verify_UNARY_NUM_OP(p[2]["type"])
            verify.verify_ERROR(t, p[2]["lineno"], lexer.find_column(p.lexer.lexdata, lexpos=p[2]["lexpos"]), "num",
                                p[2]["type"], p.lexer.lexdata[p.lexpos(1):p[2]["lastpos"]])
        p[0] = {}
        p[0]["type"] = t
        p[0]["python"] = p[1] + " " + p[2]["python"]
        p[0]["lexpos"] = p.lexpos(1)
        p[0]["lineno"] = p.lineno(1)
        p[0]["lastpos"] = p[2]["lastpos"]
        p[0]["vars"] = p[2]["vars"]
        p[0]["func_called"] = p[2]["func_called"]


def p_factor(p):
    """
    factor : LPAREN expr RPAREN
           | id
           | function_call
           | int
           | flo
           | bool
           | list 
    """
    if len(p) > 2:
        p[0] = p[2]
        p[0]["python"] = "(" + p[2]["python"] + ")"
        p[0]["lexpos"] = p.lexpos(1)
        p[0]["lineno"] = p.lineno(1)
        p[0]["lastpos"] = p.lexpos(3)
    else:
        p[0] = p[1]


def p_int(p):
    """ 
    int : INTEGER
    """
    p[0] = {}
    p[0]["type"] = "num"
    p[0]["python"] = p[1]
    p[0]["lexpos"] = p.lexpos(1)
    p[0]["lineno"] = p.lineno(1)
    p[0]["lastpos"] = p.lexpos(1) + len(p[1])
    p[0]["func_called"] = []
    p[0]["vars"] = []


def p_flo(p):
    """ 
    flo : FLOAT
    """
    p[0] = {}
    p[0]["type"] = "num"
    p[0]["python"] = p[1]
    p[0]["lexpos"] = p.lexpos(1)
    p[0]["lineno"] = p.lineno(1)
    p[0]["lastpos"] = p.lexpos(1) + len(p[1])
    p[0]["func_called"] = []
    p[0]["vars"] = []


def p_bool(p):
    """ 
    bool : BOOLEAN
    """
    p[0] = {}
    p[0]["type"] = "boolean"
    p[0]["python"] = p[1]
    p[0]["lexpos"] = p.lexpos(1)
    p[0]["lineno"] = p.lineno(1)
    p[0]["lastpos"] = p.lexpos(1) + len(p[1])
    p[0]["func_called"] = []
    p[0]["vars"] = []


def p_id(p):
    """ 
    id : IDENTIFIER
    """
    p[0] = {}
    p[0]["type"] = "any"
    p[0]["python"] = p[1]
    p[0]["lexpos"] = p.lexpos(1)
    p[0]["lineno"] = p.lineno(1)
    p[0]["lastpos"] = p.lexpos(1) + len(p[1])
    p[0]["func_called"] = []
    p[0]["vars"] = [(p[0]["lineno"], p[0]["lexpos"], p[1])]


def p_function_composition(p):
    """ 
    function_composition : id
                         | id PERIOD function_composition
    """
    p[0] = {}
    p[0]["lexpos"] = p[1]["lexpos"]
    p[0]["lineno"] = p[1]["lineno"]
    p[0]["func_called"] = [(p[1]["lineno"], p[1]["lexpos"], p[1]["python"])]
    if len(p) == 2:
        p[0]["python"] = p[1]["python"]
    else:
        p[0]["python"] = p[1]["python"] + "(" + p[3]["python"] + ")"
        p[0]["func_called"] += p[3]["func_called"]
   

def p_function_call(p):
    """ 
    function_call : function_composition LPAREN function_arguments RPAREN
                  | function_composition LPAREN RPAREN 
    """
    p[0] = {}
    p[0]["type"] = "any"
    if len(p) == 4:
        p[0]["python"] = p[1]["python"] + "()"
        p[0]["lastpos"] = p.lexpos(3) + 1
        p[0]["vars"] = []
    else:
        p[0]["python"] = p[1]["python"] + "(" + p[3]["python"] + ")" if p[1]["python"][-1] != ")" else p[1]["python"][:-1] + "(" + p[3]["python"] + "))"
        p[0]["lastpos"] = p.lexpos(4) + 1
        p[0]["vars"] = p[3]["vars"]
    p[0]["lexpos"] = p[1]["lexpos"]
    p[0]["lineno"] = p[1]["lineno"]
    p[0]["func_called"] = p[1]["func_called"]
    

def p_function_arguments(p):
    """ 
    function_arguments : expr
                       | expr COMMA function_arguments
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {}
        p[0]["python"] = p[1]["python"] + ", " + p[3]["python"]
        p[0]["lexpos"] = p[1]["lexpos"]
        p[0]["lineno"] = p[1]["lineno"]
        p[0]["vars"] = p[1]["vars"] + p[3]["vars"]
        p[0]["func_called"] = p[1]["func_called"] + p[3]["func_called"]


def p_error(p):
    column_number = lexer.find_column(p.lexer.lexdata, p)
    if p:
        raise Exception(f"{p.lineno}:{column_number}: <parse error> Unexpected token '{p.value}'")
    else:
        raise Exception(f"{p.lineno}:{column_number}: <parse error> Unexpected end of input")


parser = yacc.yacc()
parser.functions = {}
parser.warnings = []
parser.newFunctions = []
