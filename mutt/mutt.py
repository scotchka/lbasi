import sys

from parser import parser
from code_generator import CodeGenerator
from virtual_machine import VM

source_file = sys.argv[1]

with open(source_file) as f:
    source_code = f.read()


ast = parser.parse(source_code)

code_object = CodeGenerator()(ast)

# print code_object.code

VM(code_object).run()
