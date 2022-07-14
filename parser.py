from lib2to3.pgen2 import token
from tokenizer import *

out = ""

values_in_stack = 0

data_section = ""

current_line = 1

def get_token(tokens, pointer, offset):
    return tokens[pointer + offset]

def get_value(values, pointer, offset):
    return values[pointer + offset]

def make_error(message, line, suggestion=""):
    print("ERROR: " + message)
    print("LINE: " + str(line))
    if suggestion != "":
        print("SUGGESTION: " + suggestion)
    exit(1)

def parse(tokens, values):
    global out, current_line, data_section, values_in_stack

    ifs = 0
    token_pointer = 0
    entry_closed = True

    out += """section .text
global _start
"""

    data_section += '\n'
    data_section += ";; --- data ---\n"
    data_section += "section .data\n"
    data_section += "    negative_symbol db '-', 0\n"

    while token_pointer < len(tokens): 
        # Stack expression:
        if tokens[token_pointer] == STACK_EXPR:
            # Get the next token
            identifier_token = get_token(tokens, token_pointer, 1)
            # Each expression must have an identifier
            if identifier_token == IDENTIFIER:
                identifier = get_value(values, token_pointer, 1)
                # An assembly subroutine is created with the identifier as name
                out += '\n'
                out += ";; --- stackexpr ---\n"
                out += '%macro ' + identifier + ' 0\n'

                for tok in tokens[token_pointer:]:
                    if tok == INT:
                        values_in_stack += 1
                        value = get_value(values, token_pointer, 0)
                        out += 'push ' + value + '\n'

                    elif tok == ADD_OP:
                        if values_in_stack < 2:
                            make_error(
                                "Not enough values in stack to perform operation",
                                current_line
                            )
                        values_in_stack -= 2
                        tok_one = get_token(tokens, token_pointer, -1)
                        tok_two = get_token(tokens, token_pointer, -2)

                        out += ';; --- add ---\n'
                        out += 'pop rax\n'
                        out += 'pop rbx\n'
                        out += 'add rax, rbx\n'
                        out += 'push rax\n'
                        
                        values_in_stack += 1

                    elif tok == SUB_OP:
                        if values_in_stack < 2:
                            make_error(
                                "Not enough values in stack to perform operation",
                                current_line
                            )
                        values_in_stack -= 2
                        tok_one = get_token(tokens, token_pointer, -1)
                        tok_two = get_token(tokens, token_pointer, -2)
                        
                        out += ';; --- sub ---\n'
                        out += 'pop rax\n'
                        out += 'pop rbx\n'
                        out += 'sub rax, rbx\n'
                        out += 'push rax\n'

                        values_in_stack += 1 

                    elif tok == MUL_OP:
                        if values_in_stack < 2:
                            make_error(
                                "Not enough values in stack to perform operation",
                                current_line
                            )
                        values_in_stack -= 2
                        tok_one = get_token(tokens, token_pointer, -1)
                        tok_two = get_token(tokens, token_pointer, -2)

                        out += ';; --- mul ---\n'
                        out += 'pop rax\n'
                        out += 'pop rbx\n'
                        out += 'imul rbx\n'
                        out += 'push rax\n'

                        values_in_stack += 1 

                    elif tok == DIV_OP:
                        if values_in_stack < 2:
                            make_error(
                                "Not enough values in stack to perform operation",
                                current_line
                            )
                        values_in_stack -= 2
                        tok_one = get_token(tokens, token_pointer, -1)
                        tok_two = get_token(tokens, token_pointer, -2)

                        out += ';; --- div ---\n'
                        out += 'pop rax\n'
                        out += 'pop rbx\n'
                        out += 'idiv rbx\n'
                        out += 'push rax\n'

                        values_in_stack += 1 
                    
                    if tok == NEW_LINE:
                        current_line += 1

                    if tok == END:
                        break
                    
                    token_pointer += 1
            else:
                make_error(
                    "Stack expression must have an identifier", 
                    current_line,
                    "Please provide an identifier after stackexpr"
                )

            out += '%endmacro\n'
        
        elif tokens[token_pointer] == NEW_LINE:
            current_line += 1

        elif tokens[token_pointer] == ENTRY:
            entry_closed = False
            out += '\n'
            out += '_start:\n'

        elif tokens[token_pointer] == CONDITIONAL:
            if values[token_pointer] == '>':
                out += '\n'
                out += ';; --- greater than ---\n'
                out += 'mov rcx, 0\n'
                out += 'mov rdx, 1\n'
                out += 'pop rax\n'
                out += 'pop rbx\n'
                out += 'cmp rax, rbx\n'
                out += 'cmovg rcx, rdx\n'
                out += 'push rcx\n'
            elif values[token_pointer] == '<':
                out += '\n'
                out += ';; --- lower than ---\n'
                out += 'mov rcx, 0\n'
                out += 'mov rdx, 1\n'
                out += 'pop rax\n'
                out += 'pop rbx\n'
                out += 'cmp rax, rbx\n'
                out += 'cmovl rcx, rdx\n'
                out += 'push rcx\n'
            elif values[token_pointer] == '<=':
                out += '\n'
                out += ';; --- lower than or equal ---\n'
                out += 'mov rcx, 0\n'
                out += 'mov rdx, 1\n'
                out += 'pop rax\n'
                out += 'pop rbx\n'
                out += 'cmp rax, rbx\n'
                out += 'cmovle rcx, rdx\n'
                out += 'push rcx\n'
            elif values[token_pointer] == '>=':
                out += '\n'
                out += ';; --- greater than or equal ---\n'
                out += 'mov rcx, 0\n'
                out += 'mov rdx, 1\n'
                out += 'pop rax\n'
                out += 'pop rbx\n'
                out += 'cmp rax, rbx\n'
                out += 'cmovge rcx, rdx\n'
                out += 'push rcx\n'
            elif values[token_pointer] == '!=':
                out += '\n'
                out += ';; --- not equal ---\n'
                out += 'mov rcx, 0\n'
                out += 'mov rdx, 1\n'
                out += 'pop rax\n'
                out += 'pop rbx\n'
                out += 'cmp rax, rbx\n'
                out += 'cmovne rcx, rdx\n'
                out += 'push rcx\n'
            elif values[token_pointer] == '==':
                out += '\n'
                out += ';; --- equal to ---\n'
                out += 'mov rcx, 0\n'
                out += 'mov rdx, 1\n'
                out += 'pop rax\n'
                out += 'pop rbx\n'
                out += 'cmp rax, rbx\n'
                out += 'cmove rcx, rdx\n'
                out += 'push rcx\n'
                
        elif tokens[token_pointer] == IF:
            out += '\n'
            out += ';; --- if ---\n'
            out += 'pop rax\n'
            out += 'test rax, rax\n'
            out += 'jz _else_' + str(ifs) + '\n'
        
        elif tokens[token_pointer] == ENDIF:
            out += '\n'
            out += '_else_' + str(ifs) + ':\n'
            ifs += 1

        elif tokens[token_pointer] == END:
            if entry_closed == False:
                out += '\n'
                out += ';; --- exit ---\n'
                out += "mov rax, SYS_EXIT\n"
                out += "mov rdi, 0\n"
                out += "syscall\n"
                entry_closed = True

        elif tokens[token_pointer] == STACK_OP:
            if values[token_pointer] == 'dup':
                out += '\n'
                out += ';; --- dup ---'
            else:
                make_error(
                    "Stack operation not implemented yet",
                    current_line,
                    "TODO: Wait for release or head to [PUT GITHUB REPO]"
                )
                
        elif tokens[token_pointer] == CALL:
            identifier_token = get_token(tokens, token_pointer, 1)
            if identifier_token == IDENTIFIER:
                identifier = get_value(values, token_pointer, 1)
                out += '\n'
                out += ';; --- call ---\n'
                out += identifier + '\n'
            else:
                make_error(
                    "Call statement must have an identifier",
                    current_line,
                    "Please provide an identifier after call"
                )

        elif tokens[token_pointer] == INCLUDE:
            lib_token = get_token(tokens, token_pointer, 1)
            if lib_token == ASM_LIB:
                lib = get_value(values, token_pointer, 1)
                prefix = 'asm<'
                suffix = '>'
                lib = lib[len(prefix):]
                lib = lib[:-len(suffix)]
                out += "\n"
                out += ";; --- include ---\n"
                out += '%include "' + lib + '.asm"\n'
            else:
                make_error(
                    "Include statement must be followed by a library",
                    current_line,
                    "Please provide a library after include\nThere is also a chance that the library type is not yet supported"
                )

        token_pointer += 1

    if entry_closed == False:
        make_error(
            "Entry point defined but exit point not defined",
            current_line,
            "Please define an exit point using 'end'\nLine number above is not useful here"
        )

    out += '\n'
    out += ";; --- bss ---\n"
    out += "section .bss\n"
    out += "    digitSpace resb 100\n"
    out += "    digitSpacePos resb 8\n"

    out += data_section

    f = open('output.asm', 'w')
    f.write(out)
    f.close()

    return out

