/* compile with `-fno-tree-vectorize` to forbid GCC do some weird stuff */

/* array write */
#include <stdio.h>
#include <stdlib.h>

// 1GB size
#define SIZE 1024*1024*1024

__attribute__((noinline))
void arraywrite(char* arr) {
  int i = SIZE-1, r=0;
  for (; i >= 0; i-=3) {
    arr[i] = (char) i;
  }
}

int main(int argc, char **argv) {
  char* arr = (char*) malloc(SIZE);
  arraywrite(arr);
  printf("r = %d\n", arr[0]);
  return 0;
}
