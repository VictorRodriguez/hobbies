| Fibonacci function without profiling optimization | Fibonacci function after profiling optimization with -fprofile-use |
| --------------------------------------------------|------------------------------------------------------------------- |
| 0000000000001189 <B>:								| 000000000000122e <B>:												 |
| 1189:    push   %r14								| 122e:    push   %r14												 |
| 118b:    push   %r13								| 1230:    push   %r13												 |
| 118d:    push   %r12								| 1232:    push   %r12												 |
| 118f:    push   %rbp								| 1234:    push   %rbp												 |
| 1190:    push   %rbx								| 1235:    push   %rbx												 |
| 1191:    mov    %edi,%r13d						| 1236:    mov    %edi,%r13d										 |
| 1194:    lea    0xe69(%rip),%rdi  # 2004			| 1239:    lea    0xde7(%rip),%rdi  # 2027							 |
| 119b:    callq  1030 <puts@plt>					| 1240:    callq  1030 <puts@plt>									 |
| 11a0:    test   %r13d,%r13d						| 1245:    mov    $0x1,%r12d										 |
| 11a3:    jle    11df <B+0x56>						| 1230:    push   %r13												 |
| 11a5:    mov    $0x1,%r12d						| 1232:    push   %r12												 |
| 11ab:    mov    $0x0,%ebp							| 1234:    push   %rbp												 |
| 11b0:    mov    $0x1,%ebx							| 1235:    push   %rbx												 |
| 11b5:    lea    0xe56(%rip),%r14 # 2012			| 1236:    mov    %edi,%r13d										 |
| 11bc:    jmp    11c1 <B+0x38>						| 1239:    lea    0xde7(%rip),%rdi  # 2027							 |
| 11be:    mov    %eax,%r12d						| 1240:    callq  1030 <puts@plt>									 |
| 11c1:    mov    %ebp,%esi							| 1245:    mov    $0x1,%r12d										 |
| 11c3:    mov    %r14,%rdi							| 124b:    mov    $0x0,%ebp											 |
| 11c6:    mov    $0x0,%eax							| 1250:    mov    $0x1,%ebx											 |
| 11cb:    callq  1040 <printf@plt>					| 1255:    lea    0xdd9(%rip),%r14  # 2035 							 |
| 11d0:    lea    0x0(%rbp,%r12,1),%eax				| 125c:    cmp    %r13d,%ebx										 |
| 11d5:    inc    %ebx								| 125f:    jle    126a <B+0x3c>										 |
| 11d7:    mov    %r12d,%ebp						| 1261:    pop    %rbx												 |
| 11da:    cmp    %ebx,%r13d						| 1262:    pop    %rbp												 |
| 11dd:    jge    11be <B+0x35>						| 1263:    pop    %r12												 |
| 11df:    pop    %rbx								| 1265:    pop    %r13												 |
| 11e0:    pop    %rbp								| 1267:    pop    %r14												 |
| 11e1:    pop    %r12								| 1269:    retq														 |
| 11e3:    pop    %r13								| 126a:    mov    %ebp,%esi											 |
| 11e5:    pop    %r14								| 126c:    mov    %r14,%rdi											 |
| 11e7:    retq										| 126f:    mov    $0x0,%al											 |
|													| 1271:    callq   1040 <printf@plt>								 |
|													| 1276:    lea    0x0(%rbp,%r12,1),%eax								 |
|													| 127b:    inc    %ebx												 |
|													| 127d:    mov    %r12d,%ebp										 |
|													| 1280:    mov    %eax,%r12d										 |
|													| 1283:    jmp    125c <B+0x2e>										 |
|													| 1285:    nopw    %cs:0x0(%rax,%rax,1)								 |
|													| 128c:																 |
|													| 128f:    nopw    %cs:0x0(%rax,%rax,1)								 |
|													| 1296:																 |
|													| 1299:    nopl    0x0(%rax)										 |



