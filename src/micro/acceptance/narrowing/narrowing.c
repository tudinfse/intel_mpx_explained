/* complex struct with inner array;
 * this test makes out-of-bound write of inner array
 *   -- should be detected when narrowing is enabled
 */
#include <stdio.h>
#include <stdlib.h>

struct __attribute__((__packed__)) {
  int x;
  int a[10];
  int y;
} s;

__attribute__((noinline)) 
int dummy(int* p) {
  return *p;
}

int main(int argc, char **argv) {
  int r = 0;
  int* ok = (int*)&s;
  ok[11] = 42;
  r += dummy(ok);
  printf("this must be printed before error: %d %d\n", r, ok[11]);

  int* no = s.a;
  no[10] = 43;
  r += dummy(no);
  printf("this must be printed after error: %d %d\n", r, no[10]);
  return 0;
}
