```assembly
000000000000122e <B>:
122e:    push   %r14
1230:    push   %r13
1232:    push   %r12
1234:    push   %rbp
1235:    push   %rbx
1236:    mov    %edi,%r13d
1239:    lea    0xde7(%rip),%rdi  # 2027 <_IO_stdin_used+0x27>
1240:    callq  1030 <puts@plt>
1245:    mov    $0x1,%r12d
1230:    push   %r13
1232:    push   %r12
1234:    push   %rbp
1235:    push   %rbx
1236:    mov    %edi,%r13d
1239:    lea    0xde7(%rip),%rdi  # 2027 <_IO_stdin_used+0x27>
1240:    callq  1030 <puts@plt>
1245:    mov    $0x1,%r12d
124b:    mov    $0x0,%ebp
1250:    mov    $0x1,%ebx
1255:    lea    0xdd9(%rip),%r14  # 2035 _IO_stdin_used+0x35>
125c:    cmp    %r13d,%ebx
125f:    jle    126a <B+0x3c>
1261:    pop    %rbx
1262:    pop    %rbp
1263:    pop    %r12
1265:    pop    %r13
1267:    pop    %r14
1269:    retq
126a:    mov    %ebp,%esi
126c:    mov    %r14,%rdi
126f:    mov    $0x0,%al
1271:    callq   1040 <printf@plt>
1276:    lea    0x0(%rbp,%r12,1),%eax
127b:    inc    %ebx
127d:    mov    %r12d,%ebp
1280:    mov    %eax,%r12d
1283:    jmp    125c <B+0x2e>
1285:    nopw    %cs:0x0(%rax,%rax,1)
128c:
128f:    nopw    %cs:0x0(%rax,%rax,1)
1296:
1299:    nopl    0x0(%rax)
```
