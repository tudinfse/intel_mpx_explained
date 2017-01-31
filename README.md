# Intel MPX Explained

A repository containing complete experimental setup of our "Intel MPX Explained" paper:

* `raw_results`: complete unprocessed measurements, in the form of `.csv` files.
* `asm_measurements`: scripts used to measure MPX instruction latencies and throughputs.
Also, a set of scripts that prove existence of contention on Port 1.
* `src`: sources of the tested benchmark suits and case studies. (SPEC was excluded for licencing reasons)
* `experiments/exp_*_*/run.py`: scripts defining the experiment procedure
* `experiments/makefiles/`: build types
* `install`: installation scripts

### Running the experiments

For the details of how to run the experiments on your own, please, refer to the documentation of the [underlying Fex framework](https://github.com/tudinfse/fex).

### Publications

Full description of this work can be found in one of the follwing:

* [ATC paper](): shortened form of our investigation (*not yet published*)
* [Technical Report](): complete results and full discussion (*not yet published*)
* [Supporting website](https://intel-mpx.github.io/): even more detailed results, but less discussion
