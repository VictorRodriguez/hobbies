# Security Flags at GCC and its impact in performance

This basic document describe the the following security flags: 

```
Stack execution protection:             LDFLAGS="-z noexecstack"
Data relocation and protection (RELRO): LDLFAGS="-z relro -z now"
Stack-based Buffer Overrun Detection:   CFLAGS=”-fstack-protector-strong”if using GCC 4.9 or newer,
                                            otherwise CFLAGS="-fstack-protector"
Fortify source:                         CFLAGS="-O2 -D_FORTIFY_SOURCE=2"
Format string vulnerabilities:          CFLAGS="-Wformat -Wformat-security"
```

