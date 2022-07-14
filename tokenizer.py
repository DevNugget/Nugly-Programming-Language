import shlex

STRING = 'STRING'
INT = 'INT'

CONST = 'CONST'

ENTRY = 'ENTRY'
STACK_EXPR = 'STACK_EXPR'
IDENTIFIER = 'IDENTIFIER'

ADD_OP = 'ADD_OP'
SUB_OP = 'SUB_OP'
MUL_OP = 'MUL_OP'
DIV_OP = 'DIV_OP'
STACK_OP = 'STACK_OP'

C_BRACE_L = 'C_BRACE_L'
C_BRACE_R = 'C_BRACE_R'

PARAN_L = 'PARAN_L'
PARAN_R = 'PARAN_R'

IF = 'IF'
ENDIF = 'ENDIF'
CONDITIONAL = 'CONDITIONAL'

END = 'END'
NEW_LINE = 'NEW_LINE'
UNDEFINED = 'UNDEFINED'

INCLUDE = 'INCLUDE'
ASM_LIB = 'ASM_LIB'
CALL = 'CALL'

def split_file_content(file_name):
    file = open(file_name, "r")
    text = file.readlines()
    file.close()

    text_cp = []
    for txt in text:
        txt = txt.partition('\n')

        for i in txt:
            if i != "\n":
                text_split = shlex.split(i, posix=False)
            else:
                text_split = ["\n"]
            for j in text_split:
                text_cp.append(j)

    return text_cp

def tokenize(file_name):
    values = split_file_content(file_name)

    numbers = '1234567890'
    idenChars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    conditionals = ['>', '<', '>=', '<=', '==', '!=']
    stack_ops = ['dup']

    tokens = []

    token_pointer = 0
    character_pointer = 0

    while token_pointer < len(values):
        if values[token_pointer].startswith('"') and values[token_pointer].endswith('"'):
            tokens.append(STRING)
        elif values[token_pointer] == "stackexpr":
            tokens.append(STACK_EXPR)
        elif values[token_pointer] == "end":
            tokens.append(END)
        elif values[token_pointer] == "\n":
            tokens.append(NEW_LINE)
        elif values[token_pointer] == "entry":
            tokens.append(ENTRY)
        elif values[token_pointer] == "call":
            tokens.append(CALL)
        elif values[token_pointer] == "grab":
            tokens.append(INCLUDE)
        elif values[token_pointer].startswith('asm<') and values[token_pointer].endswith('>'):
            tokens.append(ASM_LIB)
        elif '-' in values[token_pointer] and not values[token_pointer] == '-':
            for i in numbers:
                if i in values[token_pointer]:
                    tokens.append(INT)
                    break
        elif values[token_pointer] in conditionals:
            tokens.append(CONDITIONAL)
        elif values[token_pointer] == 'if':
            tokens.append(IF)
        elif values[token_pointer] == 'endif':
            tokens.append(ENDIF)
        elif values[token_pointer] in stack_ops:
            tokens.append(STACK_OP)
            
        else:
            for char in values[token_pointer]:
                if char in numbers and '-' not in values[token_pointer]:
                    tokens.append(INT)
                    break
                elif char in numbers and '-' in values[token_pointer]:
                    tokens.append(INT)
                    break
                elif (char in idenChars) or (char in idenChars and char in numbers):
                    tokens.append(IDENTIFIER)
                    break
                elif char == '+':
                    tokens.append(ADD_OP)
                    break
                elif char == '-':
                    tokens.append(SUB_OP)
                    break
                elif char == '*':
                    tokens.append(MUL_OP)
                    break
                elif char == '/':
                    tokens.append(DIV_OP)
                    break
                elif char == '{':
                    tokens.append(C_BRACE_L)
                    break
                elif char == '}':
                    tokens.append(C_BRACE_R)
                    break
                elif char == '(':
                    tokens.append(PARAN_L)
                    break
                elif char == ')':
                    tokens.append(PARAN_R)
                    break
                else:
                    tokens.append(UNDEFINED)
                    break
        
        token_pointer += 1
    return tokens
