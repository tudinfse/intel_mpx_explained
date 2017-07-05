/* stress narrowing of bounds */
#include <stdio.h>
#include <stdlib.h>

// 128MB size
#define SIZE 128*1024*1024

typedef struct __attribute__((__packed__)) {
  int x;
  int a[2];
  int y;
} s_t;

__attribute__((noinline)) 
void arraywrite(s_t* arr, int idx) {
  int i = SIZE-1, r=0;
  for (; i >= 0; i--) {
    int* innerarr = arr[i].a;
    innerarr[idx] = i;
  }
}

int main(int argc, char **argv) {
  s_t* arr = (s_t*) malloc(SIZE * sizeof(s_t));
  arraywrite(arr, 0);
  printf("r = %x\n", arr);
  return 0;
}
