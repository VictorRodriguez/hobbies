#include <stdio.h>
#include <signal.h>


void custom_logger(const char *msg)
{
  fprintf(stderr, "LOG: %s", msg);
}

static void handler(int signum)
{
  custom_logger("got signal");
}

int main(int argc, const char *argv)
{
  custom_logger("started");
  signal(SIGINT, handler);
  return 0;
}

