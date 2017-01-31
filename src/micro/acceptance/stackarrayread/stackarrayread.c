/* stack array read out of bounds */
#include <stdio.h>
#include <stdlib.h>

__attribute__((noinline)) 
int dummy(int* p) {
  return *p;
}

int main(int argc, char **argv) {
  int a[10];
  int x = dummy(a);
  x += a[11];
  printf("%d\n", x);
  return 0;
}
