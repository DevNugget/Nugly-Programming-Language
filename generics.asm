%macro exit 0
    mov rax, SYS_EXIT
    mov rdi, 0
    syscall
%endmacro