/* 
 * call many mallocs/frees
 * (stress malloc/free changes for bounds creation in standard lib)
 */
#include <stdio.h>
#include <stdlib.h>

// 32MB of pointers
#define SIZE 32*1024*1024

__attribute__((noinline)) 
void dynaloc(char** ptrs) {
  int i;
  for (i = SIZE-1; i >= 0; i--) {
    ptrs[i] = (char*) malloc(8);
  }
  for (i = SIZE-1; i >= 0; i--) {
    free(ptrs[i]);
  }
}

int main(int argc, char **argv) {
  char** ptrs = (char**) malloc(SIZE*sizeof(char*));
  dynaloc(ptrs);
  printf("ptrs = %p\n", ptrs);
  return 0;
}
