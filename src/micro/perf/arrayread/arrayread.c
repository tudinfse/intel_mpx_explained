/* array read */
#include <stdio.h>
#include <stdlib.h>

// 1GB size
#define SIZE 1024*1024*1024

__attribute__((noinline))
int arrayread(char* arr) {
  int i = SIZE-1, r=0;
  for (; i >= 0; i-=2) {
    r += arr[i];
  }
  return r;
}

int main(int argc, char **argv) {
  char* arr = (char*) malloc(SIZE);
  int r = arrayread(arr);
  printf("r = %d\n", r);
  return 0;
}
