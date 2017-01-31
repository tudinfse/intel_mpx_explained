/*
 * assign bounds of the same array to many pointers
 * (stress bounds propagation during pointer assignment -- bndstx)
 */
#include <stdio.h>
#include <stdlib.h>

// 128MB of pointers = 1GB in size
#define SIZE 128*1024*1024

__attribute__((noinline))
void ptrcreation(char** ptrs, char* arr1, char* arr2, char* arr3, char* arr4, char* arr5) {
  int i = SIZE-20, r=0;
  for (; i >= 0; i--) {
      ptrs[i] = &arr1[i % 64];
      ptrs[i+2] = &arr2[i % 64];
      ptrs[i+3] = &arr3[i % 64];
      ptrs[i+4] = &arr4[i % 64];
      ptrs[i+5] = &arr5[i % 64];
  }
}

int main(int argc, char **argv) {
  char*  arr1  = (char*)  malloc(100);
  char*  arr2  = (char*)  malloc(110);
  char*  arr3  = (char*)  malloc(120);
  char*  arr4  = (char*)  malloc(130);
  char*  arr5  = (char*)  malloc(140);
  char** ptrs = (char**) malloc(SIZE*sizeof(char*));
  ptrcreation(ptrs, arr1, arr2, arr3, arr4, arr5);
  printf("r = %hd\n", ptrs[0]);
  return 0;
}
