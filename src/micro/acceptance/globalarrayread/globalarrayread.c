/* taken from https://github.com/google/sanitizers/wiki/AddressSanitizerIntelMemoryProtectionExtensions */
/* array read out of bounds */
#include <stdio.h>
#include <stdlib.h>

int g[10];

int main(int argc, char **argv) {
  int x = g[11];
  printf("%d\n", x);
  return 0;
}
