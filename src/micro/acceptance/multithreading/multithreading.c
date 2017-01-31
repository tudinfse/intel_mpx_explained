/* two threads race on one array */
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

// 1GB size
#define SIZE 1024*1024*1024

typedef struct {
  char* arr;
  int  size;
} st_t;

__attribute__((noinline))
void* arraywrite(void* stvoid) {
  st_t* st = (st_t*) stvoid;
  char* arr = st->arr;
  int size = st->size;

  int i;
  for (i = 0; i < size; i++) {
//  __atomic_store_n(arr + i, i, __ATOMIC_SEQ_CST);  /* atomics are not checked by MPX! */
    arr[i] = (char)i;
  }
  return NULL;
}

int main(int argc, char **argv) {
  char* arr = (char*) malloc(SIZE);

  pthread_t pt;
  st_t st;
  st.arr = arr; st.size = SIZE;

  if (pthread_create(&pt, NULL, arraywrite, &st)) {
    puts("Error creating thread\n");
    return 1;
  }

  arraywrite(&st);

  if (pthread_join(pt, NULL)) {
    puts("Error joining thread\n");
    return 2;
  }

  printf("r = %hd\n", arr[0]);
  return 0;
}

