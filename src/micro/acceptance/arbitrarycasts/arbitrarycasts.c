/* arbitrary casts:  int* -> char*  */
#include <stdio.h>
#include <stdlib.h>

__attribute__((noinline)) 
char dummy(char* p) {
  return *p;
}

int main(int argc, char **argv) {
  int i[10];
  char r = 0;

  char* c = (char*) i;
  r += dummy(c);
  printf("this must be printed before error: %hd %hd\n", r, c[0]);
  c[10*4] = 42;
  r += dummy(c);
  printf("this must be printed after error: %hd %hd\n", r, c[10*4]);

  return 0;
}
