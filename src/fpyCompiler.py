from parserGrammar import parser
import re 
import sys

def repl_func(match):
    matched_str = match.group(0)
    return parser.parse(matched_str)

erFPY = re.compile(r'"""FPY.+?"""', re.DOTALL)


if len(sys.argv) > 1:
    filename = sys.argv[1]
    if re.search(r'\.py$',filename):
        file = open(filename, 'r')
        lines = file.readlines()
        data = ''.join(lines)
        texto = erFPY.sub(repl_func,data)
        outputFile = open(filename, 'w')
        outputFile.write(texto)