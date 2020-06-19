#if !defined(__INTEL_COMPILER)
#error Not Intel
#endif

#include <stdio.h>

int main(int argc, char *argv[]) {
  fputs ("Success test pass\n", stdout);

  return 0;
}
