#include <stdlib.h>
#include <curl/curl.h>
int main()
{
#ifdef LIBCURL_VERSION_MAJOR
#if LIBCURL_VERSION_MAJOR > 7
  exit(1);
#elif LIBCURL_VERSION_MAJOR == 7 && LIBCURL_VERSION_MINOR >= 22
  exit(0);
#else
  exit(1);
#endif
#else
  exit(1);
#endif
}
