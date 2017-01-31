/* test libc wrappers under MPX, namely malloc() */
#include <stdio.h>
#include <stdlib.h>

__attribute__((noinline)) 
int dummy(int* p) {
  return *p;
}

int main(int argc, char **argv) {
  int size = 0, to = 0, num = 0;
  if (argc >= 4) {
    size = atoi(argv[1]);
    to   = atoi(argv[2]);
    num  = atoi(argv[3]);
  } else {
    // make it crash by default
    size = to = num = 10;
  }

  int *p = malloc(size * sizeof(size));
  p[to] = num;
  int r = dummy(p);
  printf("%d\n", r);
  return 0;
}
