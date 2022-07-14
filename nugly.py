#!/usr/bin/python
import sys
import tokenizer
import parser

file_name = sys.argv[1]

values = tokenizer.split_file_content(file_name)
tokens = tokenizer.tokenize(file_name)

print(values, tokens)

generation = parser.parse(tokens, values)
if len(sys.argv) > 2:
    if sys.argv[2] == "show":
        print('--- x86_64 ASSEMBLY ---')
        print(generation)