/* two threads race on one array and introduce false-positive #BRs */

/*
 * full MPX         -- must non-deterministically trigger #BR
 * MPX only-writes  -- must finish correctly (because readfromx
 *                     only reads from array)
 *
 * (1) Better compile at O1 to have simple non-vectorized asm
 * (2) Make sure program runs on two cores, i.e., `--num_threads 2`
 *     (I build with `./entrypoint.py -v -d run -n micro --num_threads 2 --num_runs 10 -t gcc_mpx -b multithreading_fp`)
 *     (I run with   `CHKP_RT_MODE=count CHKP_RT_PRINT_SUMMARY=1 CHKP_RT_VERBOSE=0 build/micro/perf/multithreading_fp/gcc_mpx/multithreading_fp`)
 * (3) In *correct* MPX implementation, no #BR must be output
 *       - in current GCC and ICC implementations, output is #BR sometimes
 *         which means false positives due to broken multithreading
 */

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define ITERATIONS 100
#define MAXSIZE 1000*1000
#define OBJSIZE 1024
#define OFFSET  512

char* arr[MAXSIZE];
int dummysum = 0;
char* obj1ptr = NULL;
char* obj2ptr = NULL;
int shoulddie = 0;

/*** Background thread ***/
__attribute__((noinline))
void swap(char* objptr) {
  for (int i = 0; i < MAXSIZE; i++)
     arr[i] = objptr;
}

void* background_swap(void* dummy) {
  int i = 0;
  while (1) {
    if (shoulddie) break;
    if ((i++)%2)  swap(obj1ptr);
    else          swap(obj2ptr);
  }
  return NULL;
}

/*** Main thread ***/
__attribute__((noinline))
void readarr() {
  for (int k = 0; k < ITERATIONS; k++)
    for (int i = 0; i < MAXSIZE; i++) {
      /* access all items of array (correct in-bounds) */
      dummysum += *arr[i];
    }
}

int main(int argc, char **argv) {
  char obj1[OBJSIZE] = {0x2};
  char obj2[OBJSIZE] = {0x4};

  pthread_t pt;
  obj1ptr = (char*)&obj1;
  obj2ptr = (char*)&obj2;

  /* init arr with obj1 */
  for (int i = 0; i < MAXSIZE; i++)
    arr[i] = (char*)&obj1;

  /* start background thread which swaps obj1 <-> obj2 */
  if (pthread_create(&pt, NULL, background_swap, NULL)) {
    puts("Error creating thread\n");
    return 1;
  }

  /* main thread starts reading from array */
  readarr();
  shoulddie = 1;

  if (pthread_join(pt, NULL)) {
    puts("Error joining thread\n");
    return 2;
  }

  printf("dummysum = %d\n", dummysum);
  return 0;
}
