/* taken from https://github.com/google/sanitizers/wiki/AddressSanitizerIntelMemoryProtectionExtensions */
/* array write out of bounds */
#include <stdio.h>
#include <stdlib.h>

int g[10];

__attribute__((noinline)) 
int dummy(int* p) {
  return *p;
}

int main(int argc, char **argv) {
  g[11] = 42;
  int r = dummy(g);
  printf("%d\n", r);
  return 0;
}
