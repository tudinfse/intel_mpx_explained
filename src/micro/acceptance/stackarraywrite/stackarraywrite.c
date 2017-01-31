/* stack array write out of bounds */
#include <stdio.h>
#include <stdlib.h>

__attribute__((noinline)) 
int dummy(int* p) {
  return *p;
}

int main(int argc, char **argv) {
  int a[10];
  int x = dummy(a);
  a[11] = x;
  printf("%d\n", a[11]);
  return 0;
}
