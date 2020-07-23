```assambly

000000000000122e <B>:
122e:	push   %r15
1230:	push   %r14
1232:	push   %r13
1234:	push   %r12
1236:	push   %rbp
1237:	push   %rbx
1238:	sub    $0x8,%rsp
123c:	mov    %edi,%r14d
123f:	lea    0xde1(%rip),%rdi        # 2027 <_IO_stdin_used+0x27>
1246:	callq  1030 <puts@plt>
124b:	test   %r14d,%r14d
124e:	jle    141a <B+0x1ec>
1254:	mov    $0x1,%ebx
1259:	mov    $0x0,%r12d
125f:	mov    $0x1,%ebp
1264:	lea    0xdca(%rip),%r13        # 2035 <_IO_stdin_used+0x35>
126b:	mov    %r14d,%r15d
126e:	sub    %ebp,%r15d
1271:	and    $0x7,%r15d
1275:	je     13fc <B+0x1ce>
127b:	mov    %r12d,%esi
127e:	mov    %r13,%rdi
1281:	mov    $0x0,%eax
1286:	callq  1040 <printf@plt>
128b:	lea    (%r12,%rbx,1),%eax
128f:	inc    %ebp
1291:	mov    %ebx,%r12d
1294:	cmp    %ebp,%r14d
1297:	jl     141a <B+0x1ec>
129d:	mov    %eax,%ebx
129f:	cmp    $0x1,%r15d
12a3:	je     13fc <B+0x1ce>
12a9:	cmp    $0x2,%r15d
12ad:	je     1353 <B+0x125>
12b3:	cmp    $0x3,%r15d
12b7:	je     1337 <B+0x109>
12b9:	cmp    $0x4,%r15d
12bd:	je     131c <B+0xee>
12bf:	cmp    $0x5,%r15d
12c3:	je     1301 <B+0xd3>
12c5:	cmp    $0x6,%r15d
12c9:	je     12e6 <B+0xb8>
12cb:	mov    %r12d,%esi
12ce:	mov    %r13,%rdi
12d1:	mov    $0x0,%eax
12d6:	callq  1040 <printf@plt>
12db:	lea    (%r12,%rbx,1),%edx
12df:	inc    %ebp
12e1:	mov    %ebx,%r12d
12e4:	mov    %edx,%ebx
12e6:	mov    %r12d,%esi
12e9:	mov    %r13,%rdi
12ec:	mov    $0x0,%eax
12f1:	callq  1040 <printf@plt>
12f6:	lea    (%r12,%rbx,1),%ecx
12fa:	inc    %ebp
12fc:	mov    %ebx,%r12d
12ff:	mov    %ecx,%ebx
1301:	mov    %r12d,%esi
1304:	mov    %r13,%rdi
1307:	mov    $0x0,%eax
130c:	callq  1040 <printf@plt>
1311:	lea    (%r12,%rbx,1),%esi
1315:	inc    %ebp
1317:	mov    %ebx,%r12d
131a:	mov    %esi,%ebx
131c:	mov    %r12d,%esi
131f:	mov    %r13,%rdi
1322:	mov    $0x0,%eax
1327:	callq  1040 <printf@plt>
132c:	lea    (%r12,%rbx,1),%edi
1330:	inc    %ebp
1332:	mov    %ebx,%r12d
1335:	mov    %edi,%ebx
1337:	mov    %r12d,%esi
133a:	mov    %r13,%rdi
133d:	mov    $0x0,%eax
1342:	callq  1040 <printf@plt>
1347:	lea    (%r12,%rbx,1),%r8d
134b:	inc    %ebp
134d:	mov    %ebx,%r12d
1350:	mov    %r8d,%ebx
1353:	mov    %r12d,%esi
1356:	mov    %r13,%rdi
1359:	mov    $0x0,%eax
135e:	callq  1040 <printf@plt>
1363:	lea    (%r12,%rbx,1),%r9d
1367:	inc    %ebp
1369:	mov    %ebx,%r12d
136c:	mov    %r9d,%ebx
136f:	jmpq   13fc <B+0x1ce>
1374:	mov    %ebx,%esi
1376:	mov    %r13,%rdi
1379:	mov    $0x0,%eax
137e:	callq  1040 <printf@plt>
1383:	add    %r12d,%ebx
1386:	mov    %r12d,%esi
1389:	mov    %r13,%rdi
138c:	mov    $0x0,%eax
1391:	callq  1040 <printf@plt>
1396:	add    %ebx,%r12d
1399:	mov    %ebx,%esi
139b:	mov    %r13,%rdi
139e:	mov    $0x0,%eax
13a3:	callq  1040 <printf@plt>
13a8:	add    %r12d,%ebx
13ab:	mov    %r12d,%esi
13ae:	mov    %r13,%rdi
13b1:	mov    $0x0,%eax
13b6:	callq  1040 <printf@plt>
13bb:	lea    (%r12,%rbx,1),%r15d
13bf:	mov    %ebx,%esi
13c1:	mov    %r13,%rdi
13c4:	mov    $0x0,%eax
13c9:	callq  1040 <printf@plt>
13ce:	add    %r15d,%ebx
13d1:	mov    %r15d,%esi
13d4:	mov    %r13,%rdi
13d7:	mov    $0x0,%eax
13dc:	callq  1040 <printf@plt>
13e1:	add    %ebx,%r15d
13e4:	mov    %ebx,%esi
13e6:	mov    %r13,%rdi
13e9:	mov    $0x0,%eax
13ee:	callq  1040 <printf@plt>
13f3:	add    $0x7,%ebp
13f6:	mov    %r15d,%r12d
13f9:	add    %r15d,%ebx
13fc:	mov    %r12d,%esi
13ff:	mov    %r13,%rdi
1402:	mov    $0x0,%eax
1407:	callq  1040 <printf@plt>
140c:	add    %ebx,%r12d
140f:	inc    %ebp
1411:	cmp    %ebp,%r14d
1414:	jge    1374 <B+0x146>
141a:	add    $0x8,%rsp
141e:	pop    %rbx
141f:	pop    %rbp
1420:	pop    %r12
1422:	pop    %r13
1424:	pop    %r14
1426:	pop    %r15
1428:	retq
1429:	nopw   %cs:0x0(%rax,%rax,1)
1430:
1433:	nopw   %cs:0x0(%rax,%rax,1)
143a:
143d:	nopl   (%rax)
```
