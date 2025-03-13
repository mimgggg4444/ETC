pkg update && pkg upgrade
pkg install nasm
pkg install clang
pkg install ld



termux assembly


nano hello.asm


section .data
    msg db "Hello, Termux!", 0xa  ; 출력할 문자열
    len equ $ - msg  ; 문자열 길이 계산

section .text
    global _start

_start:
    mov rax, 1      ; syscall: write (sys_write)
    mov rdi, 1      ; file descriptor: stdout
    mov rsi, msg    ; 출력할 문자열 주소
    mov rdx, len    ; 출력할 문자열 길이
    syscall         ; 시스템 호출

    mov rax, 60     ; syscall: exit (sys_exit)
    xor rdi, rdi    ; 종료 코드 0
    syscall         ; 시스템 호출



nasm -f elf64 hello.asm -o hello.o

