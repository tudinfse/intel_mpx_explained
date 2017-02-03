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

* [ATC paper](): shortened form of our investigation (*not yet submitted*)
* [Technical Report](https://arxiv.org/abs/1702.00719): complete results and full discussion
* [Supporting website](https://intel-mpx.github.io/): even more detailed results, but less discussion


### Cite us!

Technical Report:

```
@Article{Oleksenko:2017,
  author = {Oleksenko, Oleksii and Kuvaiskii, Dmitrii and Bhatotia, Pramod and Felber, Pascal and Fetzer, Christof},,
  title = {{Intel MPX Explained: An Empirical Study of Intel MPX and Software-based Bounds Checking Approaches}},
  journal   = "",
  archivePrefix = "arXiv",
  eprint = {1702.00719},
  primaryClass = "",
  year = {2017},
}
```
