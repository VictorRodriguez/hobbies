void f (int n) {
 char *d;
 if (n < 1025)
   d = alloca (n);
 else
   d = malloc (n);
 …
}
