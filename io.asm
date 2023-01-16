; input: rax as pointer
; output: print string at rax
%macro putS 1
    mov rax, %1
    mov rbx, 0
%%printLoop:
    mov cl, [rax]
    cmp cl, 0
    je %%endPrintLoop
    inc rbx
    inc rax
    jmp %%printLoop
%%endPrintLoop:
    mov rax, SYS_WRITE
    mov rdi, STDIN
    mov rsi, %1
    mov rdx, rbx
    syscall
%endmacro

%macro puti 1
    mov rax, %1
    call _printRAX
%endmacro

_printRAX:
    mov rcx, digitSpace
    mov rbx, 10
    mov [rcx], rbx
    inc rcx
    mov [digitSpacePos], rcx
 
_printRAXLoop:
    mov rdx, 0
    mov rbx, 10
    div rbx
    push rax
    add rdx, 48
 
    mov rcx, [digitSpacePos]
    mov [rcx], dl
    inc rcx
    mov [digitSpacePos], rcx
    
    pop rax
    cmp rax, 0
    jne _printRAXLoop
 
_printRAXLoop2:
    mov rcx, [digitSpacePos]
 
    mov rax, 1
    mov rdi, 1
    mov rsi, rcx
    mov rdx, 1
    syscall
 
    mov rcx, [digitSpacePos]
    dec rcx
    mov [digitSpacePos], rcx
 
    cmp rcx, digitSpace
    jge _printRAXLoop2
 
    ret

%macro putI64 0
pop rax
call print_signed_int64
%endmacro

print_signed_int64:
    test rax, rax
    js print_signed_int64_negative
    call _printRAX
    ret

print_signed_int64_negative:
    push rax
    putS negative_symbol
    pop rax
    neg rax
    call _printRAX
    ret
