from parserGrammar import parser
from parserGrammar import lexer
import re
import sys



def repl_func(match,data):
    matched_str = match.group(0) 
    start_index = match.start()
    line_num = data.count('\n', 0, start_index) +1
    lexer.lexer.lineno = line_num
    try:
        ret_str = parser.parse(matched_str)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
  
    return ret_str

erFPY = re.compile(r'"""FPY.+?"""', re.DOTALL)

if len(sys.argv) > 1:
    filename = sys.argv[1]
    if re.search(r'\.py$', filename):
        try:
            file = open(filename, 'r')
        except Exception as e:
            print(e, file=sys.stderr)
            sys.exit(1)
        lines = file.readlines()
        data = ''.join(lines)
        texto = erFPY.sub(lambda match: repl_func(match, data), data)
        outputFile = open(filename[:-3] + "FPY.py", 'w')
        outputFile.write(texto)
        warnings = sorted_list = sorted(parser.warnings, key=lambda x: (x[0], x[1]))
        for w in warnings:
            print(w[2], file=sys.stderr)
    else:
        print(f"File '{filename}' is not valid", file=sys.stderr)
else:
    print(f"File not specificated", file=sys.stderr)
