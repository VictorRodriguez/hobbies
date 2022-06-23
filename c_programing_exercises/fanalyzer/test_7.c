#include <string.h>
const char s3[] = "012.45";
int main (void) {
  char *p = strchr (s3, '.');
  *p = 0;
  return s3[3] == 0;
}
