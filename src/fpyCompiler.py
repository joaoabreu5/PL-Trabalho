from parserGrammar import parser
import re
import sys


def repl_func(match):
    matched_str = match.group(0)    
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
        texto = erFPY.sub(repl_func, data)
        outputFile = open(filename[:-3] + "FPY.py", 'w')
        outputFile.write(texto)
    else:
        print(f"File '{filename}' is not valid", file=sys.stderr)
else:
    print(f"File not specificated", file=sys.stderr)
