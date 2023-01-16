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

def check_stack_op(token):
    global out
    if token == 'dup':
        out += '\n'
        out += ';; --- dup ---\n'
        out += 'pop rax\n'
        out += 'push rax\n'
        out += 'push rax\n'
    elif token == 'swap':
        out += '\n'
        out += ';; --- swap ---\n'
        out += 'pop rax\n'
        out += 'pop rbx\n'
        out += 'push rax\n'
        out += 'push rbx\n'
    else:
        make_error(
            "Stack operation not implemented yet",
            current_line,
            "TODO: Wait for release or head to [PUT GITHUB REPO]"
        )
    
def parse(tokens, values):
    global out, current_line, data_section, values_in_stack

    ifs = 0
    whiles = 0

    end_presedence = []
    
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

                    elif tok == PLUS_PLUS:
                        if values_in_stack < 1:
                            make_error(
                                "Not enough values in stack to perform operation",
                                current_line
                            )
                        values_in_stack -= 1
                        tok_one = get_token(tokens, token_pointer, -1)
                        tok_two = get_token(tokens, token_pointer, -2)

                        out += ';; --- add (plus plus) ---\n'
                        out += 'pop rax\n'
                        out += 'mov rbx, 1\n'
                        out += 'add rax, rbx\n'
                        out += 'push rax\n'
                        
                        values_in_stack += 1
                        
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

                    elif tok == STACK_OP:
                        value = get_value(values, token_pointer, 0)
                        check_stack_op(value)
                        
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
            end_presedence.append('entry')
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

        elif tokens[token_pointer] == PLUS_PLUS:
            if values_in_stack < 1:
                make_error(
                    "Not enough values in stack to perform operation",
                    current_line
                )
            values_in_stack -= 1
            tok_one = get_token(tokens, token_pointer, -1)
            tok_two = get_token(tokens, token_pointer, -2)

            out += ';; --- add (plus plus) ---\n'
            out += 'pop rax\n'
            out += 'mov rbx, 1\n'
            out += 'add rax, rbx\n'
            out += 'push rax\n'
                        
            values_in_stack += 1
                
        elif tokens[token_pointer] == IF:
            end_presedence.append('if')
            out += '\n'
            out += ';; --- if ---\n'
            out += 'pop rax\n'
            out += 'test rax, rax\n'
            out += 'jz _else_' + str(ifs) + '\n'
            
        elif tokens[token_pointer] == WHILE:
            end_presedence.append('while')
            out += '\n'
            out += '_while_' + str(whiles) + ':\n'
            out += ';; --- while ---\n'

        elif tokens[token_pointer] == DO:
            out += '\n'
            out += ';; --- do ---\n'
            out += 'pop rax\n'
            out += 'test rax, rax\n'
            out += 'jz _else_' + str(ifs) + '\n'

        elif tokens[token_pointer] == ENDIF:
            out += '\n'
            out += '_else_' + str(ifs) + ':\n'
            ifs += 1

        elif tokens[token_pointer] == END:
            if entry_closed == False and end_presedence[-1] == 'entry':
                out += '\n'
                out += ';; --- exit ---\n'
                out += "mov rax, SYS_EXIT\n"
                out += "mov rdi, 0\n"
                out += "syscall\n"
                entry_closed = True
            elif end_presedence[-1] == 'if':
                end_presedence.pop(-1)
                out += '\n'
                out += '_else_' + str(ifs) + ':\n'
                ifs += 1
            elif end_presedence[-1] == 'while':
                end_presedence.pop(-1)
                out += '\n'
                out += 'jmp _while_' + str(whiles) + '\n'
                out += '_else_' + str(ifs) + ':\n'
                ifs += 1
                whiles += 1

        elif tokens[token_pointer] == STACK_OP:
            value = get_value(values, token_pointer, 0)
            check_stack_op(value)
        
        elif tokens[token_pointer] == CONST:
            next_tok = get_token(tokens, token_pointer, 1)
            next_next_tok = get_token(tokens, token_pointer, 2)
            if next_tok == IDENTIFIER:
                identifier = get_value(values, token_pointer, 1)
                val = get_value(values, token_pointer, 2)
                if next_next_tok == STRING:
                    data_section += '   ' + identifier + ' db ' + val + ',0'
                else:
                    data_section += '   ' + identifier + ' db ' + val

        elif tokens[token_pointer] == INVOKE:
            next_tok = get_token(tokens, token_pointer, 1)
            if next_tok == STRING:
                string_to_invoke = get_value(values, token_pointer, 1)
                string_to_invoke = string_to_invoke.removeprefix('"')
                string_to_invoke = string_to_invoke.removesuffix('"')
                string_to_invoke = string_to_invoke.removeprefix("'")
                string_to_invoke = string_to_invoke.removesuffix("'")
                out += str(string_to_invoke)
                
        #elif tokens[token_pointer] == STRING:
        #    string_val = get_value(values, token_pointer, 0)
        #    out += 'push"' + string_val + '"\n'

        elif tokens[token_pointer] == CALL:
            identifier_token = get_token(tokens, token_pointer, 1)
            if identifier_token == IDENTIFIER:
                identifier = get_value(values, token_pointer, 1)
                next_next_tok = get_token(tokens, token_pointer, 2)
                out += '\n'
                out += ';; --- call ---\n'
                if next_next_tok != INVOKE:
                    out += identifier + '\n'
                else:
                    out += identifier
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
        elif tokens[token_pointer] == INT:
            values_in_stack += 1
            value = get_value(values, token_pointer, 0)
            out += 'push ' + value + '\n'

        elif tokens[token_pointer] == ADD_OP:
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

        elif tokens[token_pointer] == SUB_OP:
            if values_in_stack < 2:
                make_error(
                    "Not enough values in stack to perform operation",
                    current_line
                )
            values_in_stack -= 2
            tok_one = get_token(tokens, token_pointer, -1)
            tok_two = get_token(tokens, token_pointer, -2)
            
            out += ';; --- sub ---\n'
            out += 'pop rbx\n'
            out += 'pop rax\n'
            out += 'sub rax, rbx\n'
            out += 'push rax\n'

            values_in_stack += 1 

        elif tokens[token_pointer] == MUL_OP:
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

        elif tokens[token_pointer] == DIV_OP:
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

