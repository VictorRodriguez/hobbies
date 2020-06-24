#include <stdio.h>

int main(void) {
  __builtin_cpu_init();
  printf("%d\n", __builtin_cpu_supports ("sse"));
  printf("%d\n", __builtin_cpu_supports ("avx"));
  printf("%d\n", __builtin_cpu_supports ("avx2"));
  printf("%d\n", __builtin_cpu_supports ("avx512dq"));
  if (__builtin_cpu_supports("avx512dq"))
	printf("has support for avx512");
  else if(__builtin_cpu_supports("avx2"))
	printf("has support for avx2");
  else
	printf("has support for sse4");
}
