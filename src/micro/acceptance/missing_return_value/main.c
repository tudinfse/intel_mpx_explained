#include <iostream>
#include <stdlib.h>
#include <pthread.h>
#include <vector>

void* entry_pt(void*);
void test();

using namespace std;


#define NUM_THREADS 2

int main (int argc, char **argv) {
	std::vector<pthread_t> threads(NUM_THREADS);

    for(int i=0; i<NUM_THREADS; i++){
		pthread_create(&threads[i], NULL, entry_pt, NULL);
	}
	for (int i=0; i<NUM_THREADS; i++){
		pthread_join(threads[i], NULL);
	}
	cout << "done" << endl;
	return 0;

}

void* entry_pt(void* data)
{
	test();
}


void test() {
    cout << "called test" << endl;
}
