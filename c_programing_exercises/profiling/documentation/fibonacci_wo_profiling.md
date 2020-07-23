```assembly
0000000000001189 <B>:
1189:    push   %r14
118b:    push   %r13
118d:    push   %r12
118f:    push   %rbp
1190:    push   %rbx
1191:    mov    %edi,%r13d
1194:    lea    0xe69(%rip),%rdi  # 2004 <_IO_stdin_used+0x4>
119b:    callq  1030 <puts@plt>
11a0:    test   %r13d,%r13d
11a3:    jle    11df <B+0x56>
11a5:    mov    $0x1,%r12d
11ab:    mov    $0x0,%ebp
11b0:    mov    $0x1,%ebx
11b5:    lea    0xe56(%rip),%r14 # 2012 <_IO_stdin_used+0x12>
11bc:    jmp    11c1 <B+0x38>
11be:    mov    %eax,%r12d
11c1:    mov    %ebp,%esi
11c3:    mov    %r14,%rdi
11c6:    mov    $0x0,%eax
11cb:    callq  1040 <printf@plt>
11d0:    lea    0x0(%rbp,%r12,1),%eax
11d5:    inc    %ebx
11d7:    mov    %r12d,%ebp
11da:    cmp    %ebx,%r13d
11dd:    jge    11be <B+0x35>
11df:    pop    %rbx
11e0:    pop    %rbp
11e1:    pop    %r12
11e3:    pop    %r13
11e5:    pop    %r14
11e7:    retq
```
