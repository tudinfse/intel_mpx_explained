#include <stdlib.h>
#include <stdio.h>

#define NUM_TABLES 30000
#define ALIGN_TO_NEW_BT 1048576

void main() {
    // create a random variable to have something to point into
    int a_variable = 5;

    // create tables
    int **pointer_addresses[NUM_TABLES];
    int i, err;
    for(i = 0; i < NUM_TABLES; i++) {
        /*
        * Allocate memory chunks aligned to 4 MB
        * so that each chunk will have a separate BT
        */
        err = posix_memalign((void **) &pointer_addresses[i], ALIGN_TO_NEW_BT, 1);

        /*
        * Store a pointer in the allocated memory
        */
        *pointer_addresses[i] = &a_variable;
    }

#ifdef FREE
    /*
    * Free memory - the corresponding BTs will be freed automatically
    */
    for(i = 0; i < NUM_TABLES; i++) {
        free(pointer_addresses[i]);
    }
#endif
}
